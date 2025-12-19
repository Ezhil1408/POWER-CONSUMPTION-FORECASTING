#!/usr/bin/env python3
"""
Test script to simulate frontend upload functionality.
"""

import os
import sys
import requests

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_upload():
    """Test the upload functionality."""
    try:
        # Create a sample CSV file
        sample_csv_content = """Year,Month,Monthly_kWh
2020,January,1250.5
2020,February,1100.2
2020,March,1300.8
2020,April,1150.3
2020,May,1400.7
2020,June,1500.9
2020,July,1600.1
2020,August,1550.4
2020,September,1450.6
2020,October,1350.8
2020,November,1200.3
2020,December,1300.7
2021,January,1280.5
2021,February,1150.2
2021,March,1350.8
2021,April,1200.3
2021,May,1450.7
2021,June,1550.9
2021,July,1650.1
2021,August,1600.4
2021,September,1500.6
2021,October,1400.8
2021,November,1250.3
2021,December,1350.7
"""
        
        # Write sample data to a file
        with open('sample_test_data.csv', 'w') as f:
            f.write(sample_csv_content)
        
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get('http://localhost:5000/health')
        print(f"Health check response: {response.status_code} - {response.json()}")
        
        # Test upload endpoint
        print("\nTesting upload endpoint...")
        with open('sample_test_data.csv', 'rb') as f:
            files = {'file': ('sample_test_data.csv', f, 'text/csv')}
            response = requests.post('http://localhost:5000/upload', files=files)
        
        print(f"Upload response status: {response.status_code}")
        print(f"Upload response: {response.json()}")
        
        # Clean up
        os.remove('sample_test_data.csv')
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error in test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_upload()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")