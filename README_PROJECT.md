Power Consumption Forecasting for Smart Grids
=================================================

This project implements a PySpark ML pipeline to forecast power consumption using historical power logs and weather data. It also describes a conceptual Scala UI to visualize results.

Quick start
-----------

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Run the forecasting app (keep Spark UI alive):

```powershell
python forecasting_app.py --power-csv data/raw/power.csv --weather-csv data/raw/weather.csv --output-dir outputs/forecasts --keep-ui
```

3. Open Spark Web UI while the job runs:

http://localhost:4040

Outputs
-------
- `outputs/forecasts/predictions.parquet`: full predictions
- `outputs/forecasts/predictions_sample.csv`: sample CSV of predictions
- `outputs/forecasts/<model-name>`: saved PipelineModel

Notes
-----
- Ensure Java is installed and on PATH (required by PySpark).
- If Spark UI disappears, rerun the job with `--keep-ui` to pause at the end until you press Enter.

Files added
-----------
- `forecasting_app.py`: runnable PySpark application meeting the project requirements.
- `scala_ui_structure.md`: conceptual Scala web app structure to consume outputs and render dashboards.
