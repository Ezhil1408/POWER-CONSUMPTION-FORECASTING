#!/bin/bash
# Script to run all services for the Power Consumption Forecasting project

echo "Starting Power Consumption Forecasting project..."

# Start Spark application in background
echo "Starting Spark application..."
python forecasting_app.py --power-csv power_consumption_2015_2024_no_building.csv --keep-ui &

# Wait a moment for Spark to start
sleep 2

# Start upload handler in background
echo "Starting upload handler..."
python web_dashboard/upload_handler.py &

# Wait a moment for upload handler to start
sleep 2

# Start web server in background
echo "Starting web server..."
cd web_dashboard && python -m http.server 8000 &

echo ""
echo "=================================================="
echo "PROJECT READY!"
echo "=================================================="
echo "Access the web dashboard at: http://localhost:8000"
echo "Spark UI available at: http://localhost:4040 or http://localhost:4041"
echo "Upload handler API at: http://localhost:5000"
echo ""
echo "Login credentials:"
echo "  Username: admin"
echo "  Password: password"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================================="
echo ""

# Wait for all background processes
wait