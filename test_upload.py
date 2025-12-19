#!/usr/bin/env python3
"""
Test script to debug the upload functionality.
"""

import os
import sys
import tempfile
import pandas as pd

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the forecasting modules
from src.preprocessing.data_loader import load_power_data
from src.preprocessing.feature_engineering import create_features
from src.models.train import train_model
from src.models.predict import make_predictions
from src.models.evaluation import evaluate_model
from src.utils.spark_session import create_spark_session

def test_processing():
    """Test the processing pipeline with a sample file."""
    try:
        # Create a sample CSV file
        sample_data = {
            'Year': [2020, 2020, 2020, 2021, 2021, 2021],
            'Month': ['January', 'February', 'March', 'January', 'February', 'March'],
            'Monthly_kWh': [1250.5, 1100.2, 1300.8, 1280.5, 1150.2, 1350.8]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Save to temporary file
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, 'test_data.csv')
        df.to_csv(file_path, index=False)
        
        print(f"Created test file at: {file_path}")
        
        # Create Spark session
        spark = create_spark_session("PowerForecast_Test")
        print("Created Spark session")
        
        # Load the data
        power_data = load_power_data(spark, file_path)
        print("Loaded power data")
        power_data.show()
        
        # Create features
        features = create_features(power_data)
        print("Created features")
        features.show()
        
        # Split into train/test
        train_df, test_df = features.randomSplit([0.8, 0.2], seed=42)
        print("Split data")
        print(f"Train size: {train_df.count()}, Test size: {test_df.count()}")
        
        # Train model
        model = train_model(train_df)
        print("Trained model")
        
        # Predict on test
        predictions = make_predictions(model, test_df)
        print("Made predictions")
        predictions.show()
        
        # Evaluate
        metrics = evaluate_model(predictions)
        print("Evaluated model")
        print(f"Metrics: {metrics}")
        
        # Stop Spark session
        spark.stop()
        
        # Clean up
        os.remove(file_path)
        os.rmdir(temp_dir)
        
        print("Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_processing()