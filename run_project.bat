@echo off
cd /d %~dp0
start "Spark UI" python forecasting_app.py --power-csv power_consumption_2015_2024_no_building.csv --keep-ui
start "Upload Handler" python web_dashboard\upload_handler.py
cd web_dashboard
start "Web Dashboard" python -m http.server 8000
echo Spark UI will be available at http://localhost:4040 (or next available port)
echo Upload Handler will be available at http://localhost:5000
echo Web Dashboard will be available at http://localhost:8000
echo.
echo To upload and process your own data, navigate to the "Predictions" page in the web dashboard.
pause