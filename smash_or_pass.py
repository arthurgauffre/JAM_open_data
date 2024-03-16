#!/usr/bin/env python3

import subprocess

def generate_city_description(city_name):
    prompt = f"créer une description de max 200 caractères sur la ville de {city_name}."
    command_output = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True).stdout.decode('utf-8')
    return command_output

if __name__ == "__main__":
    print("Welcome to the city data program!")