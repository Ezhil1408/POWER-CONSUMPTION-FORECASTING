"""Power Consumption Forecasting Spark Application

Usage (example):
  python forecasting_app.py \
    --power-csv data/raw/power.csv \
    --weather-csv data/raw/weather.csv \
    --output-dir outputs/forecasts --keep-ui

This script reads power and weather CSVs, performs feature engineering,
trains a GBT regressor with Spark MLlib, saves predictions and model,
and prints RMSE/MAE. Use `--keep-ui` to keep the Spark UI alive until you
press Enter (so you can inspect http://localhost:4040).
"""
import argparse
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, dayofweek, month, to_timestamp, trim, lower, concat, lit, when
from pyspark.sql.window import Window
from pyspark.sql.functions import lag
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--power-csv", required=True, help="Power usage CSV with timestamp and power columns")
    p.add_argument("--weather-csv", required=False, help="Weather CSV with timestamp and temp/humidity/cloud columns")
    p.add_argument("--output-dir", default="outputs/forecasts", help="Directory to write predictions and model")
    p.add_argument("--keep-ui", action="store_true", help="Keep Spark UI running until Enter pressed")
    p.add_argument("--model-name", default="gbt_model", help="Name for saved model directory")
    return p.parse_args()


def load_csv(spark, path, schema_infer=True):
    return spark.read.csv(path, header=True, inferSchema=schema_infer)


def create_features(df_power, df_weather=None):
    # Ensure timestamp column exists and is of timestamp type
    if "timestamp" in df_power.columns:
        df = df_power.withColumn("timestamp", to_timestamp(col("timestamp")))
    elif "Year" in df_power.columns and "Month" in df_power.columns:
        # normalize Month into numeric (accept names like 'Jan' or numbers)
        month_col = trim(lower(col("Month")))
        month_map = {
            'jan': 1, 'january': 1,
            'feb': 2, 'february': 2,
            'mar': 3, 'march': 3,
            'apr': 4, 'april': 4,
            'may': 5,
            'jun': 6, 'june': 6,
            'jul': 7, 'july': 7,
            'aug': 8, 'august': 8,
            'sep': 9, 'sept': 9, 'september': 9,
            'oct': 10, 'october': 10,
            'nov': 11, 'november': 11,
            'dec': 12, 'december': 12
        }
        m = month_col
        month_expr = None
        for name, idx in month_map.items():
            if month_expr is None:
                month_expr = when(m == name, idx)
            else:
                month_expr = month_expr.when(m == name, idx)
        month_expr = month_expr.otherwise(when(col("Month").cast("int").isNotNull(), col("Month").cast("int")).otherwise(None))
        df = df_power.withColumn("Month", month_expr)
        df = df.withColumn("Year", col("Year").cast("int"))
        # create synthetic timestamp from Year-Month-01
        df = df.withColumn("timestamp", to_timestamp(concat(col("Year"), lit("-"), col("Month"), lit("-01")), "yyyy-M-d"))
    else:
        raise ValueError("power CSV must contain a 'timestamp' column or 'Year' and 'Month' columns")

    # rename power column if needed
    power_candidates = [c for c in df.columns if c.lower() in ("power", "power_draw", "mw", "value", "usage", "power_usage")]
    if power_candidates:
        power_col = power_candidates[0]
        df = df.withColumnRenamed(power_col, "power")
    elif "Monthly_kWh" in df.columns:
        df = df.withColumnRenamed("Monthly_kWh", "power")
    else:
        raise ValueError("power CSV must contain a numeric power column (e.g. 'power' or 'Monthly_kWh')")

    # temporal features
    df = df.withColumn("hour", hour(col("timestamp")))
    df = df.withColumn("day_of_week", dayofweek(col("timestamp")))
    df = df.withColumn("month", month(col("timestamp")))

    # lagged feature (previous period's power). Order by timestamp
    w = Window.orderBy("timestamp")
    df = df.withColumn("lag1_power", lag("power", 1).over(w))

    # join weather if provided (exact timestamp join)
    if df_weather is not None:
        if "timestamp" in df_weather.columns:
            df_weather = df_weather.withColumn("timestamp", to_timestamp(col("timestamp")))
        # attempt to normalize common weather column names
        weather_cols = {}
        for c in df_weather.columns:
            lc = c.lower()
            if "temp" in lc:
                weather_cols[c] = "temperature"
            if "humid" in lc:
                weather_cols[c] = "humidity"
            if "cloud" in lc or "cover" in lc:
                weather_cols[c] = "cloud_cover"
        for orig, new in weather_cols.items():
            df_weather = df_weather.withColumnRenamed(orig, new)
        df = df.join(df_weather.select("timestamp", *[c for c in df_weather.columns if c != "timestamp"]), on="timestamp", how="left")

    # keep only relevant numeric columns and drop nulls
    candidate_features = ["hour", "day_of_week", "month", "lag1_power", "temperature", "humidity", "cloud_cover"]
    available = [c for c in candidate_features if c in df.columns]
    df = df.select("timestamp", "power", *available)
    df = df.na.drop(subset=["power"])
    # fill missing feature values (simple) with 0 or mean could be used; here use 0
    df = df.fillna(0)
    # rename target
    df = df.withColumnRenamed("power", "target")
    return df


def train_and_evaluate(df, output_dir, model_name="gbt_model"):
    # split
    train, test = df.randomSplit([0.8, 0.2], seed=42)

    # select numeric feature columns
    numeric = [name for name, dtype in train.dtypes if name != "target" and dtype in ("int", "bigint", "double", "float")]
    if not numeric:
        raise RuntimeError("No numeric features available for training")

    assembler = VectorAssembler(inputCols=numeric, outputCol="features")
    gbt = GBTRegressor(featuresCol="features", labelCol="target", maxIter=50)
    pipeline = Pipeline(stages=[assembler, gbt])

    model = pipeline.fit(train)
    predictions = model.transform(test)

    rmse_eval = RegressionEvaluator(labelCol="target", predictionCol="prediction", metricName="rmse")
    mae_eval = RegressionEvaluator(labelCol="target", predictionCol="prediction", metricName="mae")
    rmse = rmse_eval.evaluate(predictions)
    mae = mae_eval.evaluate(predictions)

    # save outputs
    os.makedirs(output_dir, exist_ok=True)
    preds_path = os.path.join(output_dir, "predictions.parquet")
    predictions.select("timestamp", "target", "prediction").write.mode("overwrite").parquet(preds_path)

    # also write CSV sample
    sample_csv = os.path.join(output_dir, "predictions_sample.csv")
    predictions.select("timestamp", "target", "prediction").limit(500).toPandas().to_csv(sample_csv, index=False)

    model_path = os.path.join(output_dir, model_name)
    # PipelineModel save
    model.write().overwrite().save(model_path)

    metrics = {"RMSE": rmse, "MAE": mae}
    return metrics, preds_path, model_path


def main():
    args = parse_args()
    spark = SparkSession.builder.appName("PowerConsumptionForecasting").getOrCreate()

    power_df = load_csv(spark, args.power_csv)
    weather_df = None
    if args.weather_csv:
        weather_df = load_csv(spark, args.weather_csv)

    df = create_features(power_df, weather_df)
    metrics, preds_path, model_path = train_and_evaluate(df, args.output_dir, args.model_name)
    print("Model Evaluation Metrics:", metrics)

    return spark, metrics


if __name__ == "__main__":
    import sys
    spark, metrics = main()
    if "--keep-ui" in sys.argv:
        print("Spark Web UI available at http://localhost:4040. Press Enter to stop.")
        try:
            input()
        except KeyboardInterrupt:
            pass
    spark.stop()
