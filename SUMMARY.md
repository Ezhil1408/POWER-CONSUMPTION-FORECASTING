# Power Consumption Forecasting for Smart Grids - Summary

## Project Overview

This project implements a data-driven system for predicting electricity usage in smart grids using historical consumption data and machine learning techniques. The system leverages PySpark for efficient big data processing and model training.

## Key Features

- **Data Processing**: Efficient loading and preprocessing of large-scale power consumption datasets
- **Feature Engineering**: Automatic creation of temporal features (hour, day of week, month) and lagged features
- **Machine Learning**: Gradient Boosted Tree (GBT) regression model for accurate forecasting
- **Model Evaluation**: Comprehensive metrics including RMSE and MAE
- **Web Dashboard**: Interactive web interface for visualization and monitoring
- **Spark UI Integration**: Real-time monitoring of Spark jobs and performance

## Architecture

### Project Structure
```
power-consumption-forecasting-for-smart-grids/
├── src/
│   ├── main.py                 # Main entry point
│   ├── preprocessing/
│   │   ├── data_loader.py      # Data loading utilities
│   │   ├── feature_engineering.py  # Feature creation
│   │   └── weather_integration.py  # Weather data integration
│   ├── models/
│   │   ├── train.py            # Model training
│   │   ├── predict.py          # Prediction logic
│   │   └── evaluation.py       # Model evaluation
│   └── utils/
│       └── spark_session.py    # Spark session management
├── web_dashboard/              # Web interface
├── configs/                    # Configuration files
├── outputs/                    # Model outputs and predictions
└── run_project.bat             # Windows batch runner
```

### Technologies Used

- **PySpark**: Distributed data processing and ML
- **Python**: Core programming language
- **Pandas/NumPy**: Data manipulation
- **Scikit-learn**: Additional ML utilities
- **HTML/CSS/JavaScript**: Web dashboard
- **YAML**: Configuration management

## Installation & Setup

1. **Prerequisites**: Python 3.7+, Java 8+, PySpark
2. **Dependencies**: Install via `pip install -r requirements.txt`
3. **Data**: Place CSV files in the project root directory

## Usage

### Running the Project

**Option 1: Batch File (Windows)**
```bash
run_project.bat
```

**Option 2: Command Line**
```bash
python -m src.main --keep-ui
```

### Web Interfaces

- **Spark UI**: http://localhost:4040 (job monitoring)
- **Web Dashboard**: http://localhost:8000 (visualization)

## Model Performance

Current model achieves:
- **RMSE**: 74.28
- **MAE**: 62.43

These metrics indicate good predictive accuracy for power consumption forecasting.

## Key Components

### Data Pipeline
1. **Data Loading**: CSV ingestion with schema inference
2. **Feature Engineering**: Temporal and lagged feature creation
3. **Train/Test Split**: 80/20 split with random seed
4. **Model Training**: GBT regressor with 50 iterations
5. **Evaluation**: RMSE and MAE calculation

### Spark Configuration
- Local mode execution with optimized memory settings
- UI enabled for real-time monitoring
- Event logging disabled for local development

## Future Enhancements

- Weather data integration
- Real-time prediction capabilities
- Advanced ML algorithms (LSTM, Prophet)
- Cloud deployment options
- API endpoints for external integration

## Contributing

The project follows modular architecture with clear separation of concerns, making it easy to extend and contribute new features.

## License

This project is licensed under the MIT License.
