import requests
import json

API_KEY = "ttOr9sRK0Yd5"
PROJECT_TOKEN = "tFWNzeefNv9g"
RUN_TOKEN = "t-Uk8Ei-QRBe"

# Authentication for GET request // This acquires the data I scraped using Parsehub 
response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
data = json.loads(response.text)

# Class that allows me to pull specific data from API
class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()

    def get_data(self): # Method that can be called to update data
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
        self.data = json.loads(response.text)

    def get_total_cases(self):
        data = self.data['total']

        for content in data: # For loop that checks if the name is equal to coronavirus cases it will return the value
            if content['name'] == "Coronavirus Cases:":
                return content['value']
    
    def get_total_deaths(self):
        data = self.data['total']

        for content in data: # For loop that checks if the name is equal to coronavirus cases it will return the value
            if content['name'] == "Deaths:":
                return content['value']
            
            return "0"
    
    def get_country_data(self, country):
        data = self.data["country"]
        
        for content in data: # For loop that checks if the name is equal to coronavirus deaths it will return the value
            if content['name'].lower() == country.lower():
                return content
            
            return "0"
            
data = Data(API_KEY, PROJECT_TOKEN)
