#!/usr/bin/env python3

import json
import subprocess
import requests

def save_city_data(data):
    with open('city_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_city_data():
    try:
        with open('city_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_likes(likes):
    with open('city_likes.json', 'w') as file:
        json.dump(likes, file, indent=4)

def load_likes():
    try:
        with open('city_likes.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def generate_city_description(city_name):
    prompt = f"créer une description de max 200 caractères sur la ville de {city_name}."
    command_output = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True).stdout.decode('utf-8')
    return command_output


def get_random_city():
    url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records'
    params = {
        'select': 'name, coordinates, population',
        'where': 'country_code = "FR" and population > 56000',
        'limit': 100,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        save_city_data(data)
        print("City data saved successfully.")
    else:
        print("La requête a échoué avec le code :", response.status_code)

def parse_json_and_save(json_data, output_file):
    # Parse the JSON data
    data = json.loads(json_data)
    
    # Extract relevant information
    results = data['results']
    
    # Open a new text file for writing
    with open(output_file, 'w') as file:
        # Write each city's information to the file
        for city in results:
            name = city['name']
            coordinates = city['coordinates']
            population = city['population']
            like = city['like']
            file.write(f"Name: {name}\n")
            file.write(f"Coordinates: {coordinates}\n")
            file.write(f"Population: {population}\n")
            file.write(f"Like: {like}\n\n")

if __name__ == "__main__":
    get_random_city()
