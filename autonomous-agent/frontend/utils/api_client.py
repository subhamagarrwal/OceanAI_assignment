import requests
import json
import os

# Detect if running in Docker by checking for Docker hostname
# In Docker, we use the service name as hostname; locally we use localhost
def get_backend_url():
    if "BACKEND_API_URL" in os.environ:
        return os.getenv("BACKEND_API_URL")
    return "http://localhost:8000"
    
BASE_URL = get_backend_url()

class APIClient:
    @staticmethod
    def upload_files(files):
        # files is a list of ('files', open_file_object) tuples
        try:
            response = requests.post(f"{BASE_URL}/upload", files=files)
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def generate_plan(requirement: str):
        try:
            response = requests.post(f"{BASE_URL}/plan", json={"requirement": requirement})
            if response.status_code == 200:
                return response.json()
            return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def generate_code(test_case: dict):
        try:
            response = requests.post(f"{BASE_URL}/code", json={"test_case": test_case})
            if response.status_code == 200:
                return response.json().get("code", "")
            return f"# Error: {response.text}"
        except Exception as e:
            return f"# Error: {str(e)}"
