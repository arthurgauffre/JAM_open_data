#!/usr/bin/env python3

import json
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

def get_random_city():
    url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records'
    params = {
        'select': 'name, coordinates, population',
        'where': 'country_code = "FR" and population > 10000',
        'limit': 100,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        save_city_data(data)
        print("City data saved successfully.")
    else:
        print("La requête a échoué avec le code :", response.status_code)

if __name__ == "__main__":
    get_random_city()
