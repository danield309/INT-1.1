import requests
import json

API_KEY = "ttOr9sRK0Yd5"
PROJECT_TOKEN = "tFWNzeefNv9g"
RUN_TOKEN = "t-Uk8Ei-QRBe"

# Authentication for GET request // This acquires the data I scraped using Parsehub 
response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
data = json.loads(response.text)
