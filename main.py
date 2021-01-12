import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

API_KEY = "ttOr9sRK0Yd5"
PROJECT_TOKEN = "tFWNzeefNv9g"
RUN_TOKEN = "t-Uk8Ei-QRBe"

class Data:
	def __init__(self, api_key, project_token):
		self.api_key = api_key
		self.project_token = project_token
		self.params = {
			"api_key": self.api_key
		}
		self.data = self.get_data()

	def get_data(self): # Method that can be called to update data
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
		data = json.loads(response.text)
		return data

	def get_total_cases(self):
		data = self.data['total']

		for content in data: # For loop that checks if the name is equal to coronavirus cases it will return the value
			if content['name'] == "Coronavirus Cases:":
				return content['value']

	def get_total_deaths(self):
		data = self.data['total']

		for content in data: # For loop that checks if the name is equal to coronavirus deaths it will return the value
			if content['name'] == "Deaths:":
				return content['value']

		return "0"

	def get_country_data(self, country):
		data = self.data["country"]

		for content in data:
			if content['name'].lower() == country.lower():
				return content

		return "0"

	def get_list_of_countries(self): # Print list of countries with COVID cases
		countries = []
		for country in self.data['country']:
			countries.append(country['name'].lower())

		return countries

	def update_data(self):
		response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

		def poll():
			time.sleep(0.1)
			old_data = self.data
			while True:
				new_data = self.get_data()
				if new_data != old_data:
					self.data = new_data
					print("Data updated..") # Shows when data is finalized with an update
					break
				time.sleep(5)


		t = threading.Thread(target=poll)
		t.start()


# Voice Assistant methods start here

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
			print("Did not recognize. Try again!", str(e)) # Return nothing if the assitant doesn't understand

	return said.lower()


def main():
	print("Started Program") # Shows on program start
	data = Data(API_KEY, PROJECT_TOKEN)
	END_PHRASE = "stop" # Use this word to stop the program 
	country_list = data.get_list_of_countries()

	TOTAL_PATTERNS = { # voice patterns that will get replies for total questions
					re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
					re.compile("[\w\s]+ total cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"): data.get_total_deaths
					}

	COUNTRY_PATTERNS = { # voice patterns that will get replies for country specific questions
					re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
					}

	UPDATE_COMMAND = "update" # Update data command

	while True:
		print("Listening...") # Shows on every loop, if a response is recorded program responds
		text = get_audio()
		print(text)
		result = None

		for pattern, func in COUNTRY_PATTERNS.items(): # Loops through COUNTRY_PATTERNS to see if they match
			if pattern.match(text):
				words = set(text.split(" "))
				for country in country_list:
					if country in words:
						result = func(country)
						break

		for pattern, func in TOTAL_PATTERNS.items(): # Loops through TOTAL_PATTERNS to see if they match
			if pattern.match(text):
				result = func()
				break

		if text == UPDATE_COMMAND: # Shows when data is being updated
			result = "Data is being updated..!"
			data.update_data()

		if result:
			speak(result)

		if text.find(END_PHRASE) != -1:  # Stop loop
			print("Exit")
			break

main()