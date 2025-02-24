import requests
import json

# Base URL for the microservice
BASE_URL = "http://127.0.0.1:5000"

# Test: Log Workout Data
def test_log_workout():
    url = f"{BASE_URL}/log_workout"
    data = {
        "user_id": "123",
        "steps": 8000,
        "calories": 300,
        "workout_duration": 45
    }

    response = requests.post(url, json=data)
    print("Log Workout Response:", response.json())

# Test: Fetch Fitness Insights
def test_fitness_insights():
    url = f"{BASE_URL}/fitness_insights?user_id=123"
    
    response = requests.get(url)
    print("Fitness Insights Response:", response.json())

# Run tests
if __name__ == "__main__":
    print("Testing Fitness Log Analytics Microservice...\n")
    test_log_workout()
    test_fitness_insights()
