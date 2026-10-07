import httpx
import time
import subprocess
import os
import sys

def main():
    # Start the FastAPI server in the background
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ['PYTHONPATH'] = backend_dir
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8080"],
        cwd=backend_dir
    )
    
    try:
        # Wait for server to start
        time.sleep(3)
        
        # Test 1: Health
        print("Testing GET /api/health...")
        r = httpx.get("http://localhost:8080/api/health")
        print("Status:", r.status_code)
        print("Response:", r.json())
        print("-" * 40)
        
        # Test 2: Predict using a real row from dataset
        print("Testing POST /api/predict...")
        payload = {
            "temperature": 27.5,
            "humidity": 45.0,
            "soil_moisture": 30.0,
            "light": 1200,
            "day": 5,
            "time_in_hours": 12.0
        }
        r = httpx.post("http://localhost:8080/api/predict", json=payload)
        print("Status:", r.status_code)
        print("Response:", r.json())
        print("-" * 40)
        
    finally:
        process.terminate()
        process.wait()

if __name__ == '__main__':
    main()
