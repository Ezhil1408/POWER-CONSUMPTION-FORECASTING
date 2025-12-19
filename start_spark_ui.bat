@echo off
echo Starting Spark UI for Power Consumption Forecasting...
echo This will start the Spark application and keep the UI available at http://localhost:4040
echo Press Enter in the command window when you want to stop Spark.
echo.
echo If you see Java errors, make sure Java 8+ and Python 3.7+ are installed.
echo.

REM Check if we're in the right directory
if not exist "forecasting_app.py" (
    echo Error: forecasting_app.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Find the most appropriate CSV file to use
if exist "web_dashboard\electricity_consumption_2015_2024.csv" (
    set CSV_FILE=web_dashboard\electricity_consumption_2015_2024.csv
) else if exist "power_consumption_2015_2024_no_building.csv" (
    set CSV_FILE=power_consumption_2015_2024_no_building.csv
) else if exist "data\raw\*.csv" (
    REM Use the first CSV file found in data/raw
    for %%f in (data\raw\*.csv) do (
        set CSV_FILE=%%f
        goto :found_csv
    )
) else (
    echo Error: No suitable CSV file found for training.
    echo Please ensure you have electricity_consumption_2015_2024.csv in web_dashboard folder
    echo or power_consumption_2015_2024_no_building.csv in the project root.
    pause
    exit /b 1
)

:found_csv
echo Using CSV file: %CSV_FILE%
echo.

REM Start the Spark application with UI
python forecasting_app.py --power-csv "%CSV_FILE%" --keep-ui

echo.
echo Spark UI has been stopped.
pause
