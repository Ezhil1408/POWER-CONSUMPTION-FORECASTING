# PowerShell script to start Spark UI for Power Consumption Forecasting
Write-Host "Starting Spark UI for Power Consumption Forecasting..." -ForegroundColor Green
Write-Host "This will start the Spark application and keep the UI available at http://localhost:4040" -ForegroundColor Yellow
Write-Host "Press Enter in the PowerShell window when you want to stop Spark." -ForegroundColor Yellow
Write-Host ""
Write-Host "If you see Java errors, make sure Java 8+ and Python 3.7+ are installed." -ForegroundColor Yellow
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "forecasting_app.py")) {
    Write-Host "Error: forecasting_app.py not found. Please run this script from the project root directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Find the most appropriate CSV file to use
$csvFile = $null
if (Test-Path "web_dashboard\electricity_consumption_2015_2024.csv") {
    $csvFile = "web_dashboard\electricity_consumption_2015_2024.csv"
} elseif (Test-Path "power_consumption_2015_2024_no_building.csv") {
    $csvFile = "power_consumption_2015_2024_no_building.csv"
} else {
    # Look for CSV files in data/raw directory
    $csvFiles = Get-ChildItem -Path "data\raw" -Filter "*.csv" -ErrorAction SilentlyContinue
    if ($csvFiles) {
        $csvFile = $csvFiles[0].FullName
    }
}

if (-not $csvFile) {
    Write-Host "Error: No suitable CSV file found for training." -ForegroundColor Red
    Write-Host "Please ensure you have electricity_consumption_2015_2024.csv in web_dashboard folder" -ForegroundColor Red
    Write-Host "or power_consumption_2015_2024_no_building.csv in the project root." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Using CSV file: $csvFile" -ForegroundColor Cyan
Write-Host ""

# Start the Spark application with UI
try {
    & python forecasting_app.py --power-csv $csvFile --keep-ui
} catch {
    Write-Host "Error running Spark application: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Spark UI has been stopped." -ForegroundColor Green
Read-Host "Press Enter to exit"
