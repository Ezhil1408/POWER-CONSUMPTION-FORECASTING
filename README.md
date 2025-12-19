# Power Consumption Forecasting for Smart Grids

This project predicts electricity usage using machine learning. It comes with a web dashboard where you can upload your own data and see predictions.

## Features

- **Power Consumption Forecasting**: Predict future energy usage based on historical data
- **Data Visualization**: Interactive charts and graphs for data exploration
- **Model Training**: Automatic model training with Gradient Boosted Trees
- **Apartment-Specific Forecasting**: Specialized support for multi-unit residential buildings with data for up to 10 houses per apartment complex
- **Real-time Processing**: Fast data upload and processing with progress tracking
- **Authentication**: Secure login system for accessing the dashboard

## Getting Started

## Quick Start - Run the Project

### Option 1: Single Command (Easiest Method):

**For Windows:**
```
run_project.bat
```

**For Mac/Linux:**
```
chmod +x run_all.sh
./run_all.sh
```

This will automatically start:
- Main forecasting application (Spark)
- Upload handler (backend)
- Web server (frontend)

Then open your browser at http://localhost:8000

### Option 2: Manual Method (Advanced Users):

Open **three separate Command Prompt/Terminal windows** and run one command in each:

**Window 1** - Main Application:
```
python forecasting_app.py --power-csv power_consumption_2015_2024_no_building.csv --keep-ui
```

**Window 2** - Web Backend:
```
cd web_dashboard
python upload_handler.py
```

**Window 3** - Web Frontend:
```
cd web_dashboard
python -m http.server 8000
```

Then open your browser at http://localhost:8000

## How to Use the Web Dashboard

1. Go to http://localhost:8000
2. Login with:
   - Username: admin
   - Password: password
3. Click on "Predictions" tab
4. Upload your CSV file (must have columns: Year, Month, Monthly_kWh)
5. Click "Upload and Process Data"
6. See your predictions!

## Need Help?

- Make sure you have Python and Java installed
- If something doesn't work, close all Command Prompt windows and try again
- Check that no other programs are using ports 4040/4041, 5000, or 8000
- If you see "port already in use" messages, the system will automatically try the next available port

## Project Structure

```
power-consumption-forecasting-for-smart-grids/
├── forecasting_app.py          # Main program
├── run_project.bat             # Single command to run everything (Windows)
├── run_all.sh                  # Single command to run everything (Mac/Linux)
├── web_dashboard/              # Website files
│   ├── upload_handler.py       # Handles file uploads
│   ├── index.html              # Home page
│   ├── predictions.html        # Predictions page (with upload)
│   └── ...                     # Other web pages
├── src/                        # Machine learning code
├── data/                       # Put your data files here
└── requirements.txt            # List of needed programs
```

## License

This project is licensed under the MIT License.