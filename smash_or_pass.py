#!/usr/bin/env python3

import json
import sys
import requests

def print_json_content(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        print(json.dumps(data, indent=4))

def get_random_city():
    url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records?where=country_code%20%3D%20%22FR%22%20and%20population%20%3E%2010000&limit=100'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("La requête a échoué avec le code :", response.status_code)


if __name__ == "__main__":
    get_random_city()