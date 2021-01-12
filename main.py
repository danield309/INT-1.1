import requests
import json
import pyttsx3
import speech_recognition as sr
import re

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
    
    def get_list_of_countries(self): # Print list of countries with COVID cases
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())
        
        return countries

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source: # Using mic from source send to said var and use google assistant to relay results
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e)) # Return nothing if the assitant doesn't understand
        
    return said.lower()

def main():
	print("Started Program")
	data = Data(API_KEY, PROJECT_TOKEN)
	END_PHRASE = "stop"

	TOTAL_PATTERNS = {
					re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
					re.compile("[\w\s]+ total cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"): data.get_total_deaths
					}

	while True:
		print("Listening...")
		text = get_audio()
		print(text)
		result = None

		for pattern, func in TOTAL_PATTERNS.items():
			if pattern.match(text):
				result = func()
				break

		if result:
			speak(result)

		if text.find(END_PHRASE) != -1:  # Stop loop
			print("Exit")
			break

main()