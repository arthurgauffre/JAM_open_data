#!/usr/bin/env python3

import subprocess
import pygame
import sys
import random
import json

def generate_city_description(city_name):
    prompt = f"créer une description de max 200 caractères sur la ville de {city_name}."
    command_output = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True).stdout.decode('utf-8')
    return command_output

def read_file_info(filename):
    cities_info = []

    with open(filename, 'r') as file:
        city_info = {}
        for line in file:
            line = line.strip()
            if line.startswith('Name:'):
                city_info['Name'] = line.split(': ')[1]
            elif line.startswith('Coordinates:'):
                coords_str = line.split(': ')
                if len(coords_str) == 2:
                    lon_lat_str = coords_str[1].strip('{}').split(', ')
                    if len(lon_lat_str) == 2:
                        lon, lat = map(float, lon_lat_str)
                        city_info['Coordinates'] = {'lon': lon, 'lat': lat}
            elif line.startswith('Population:'):
                population_str = line.split(': ')
                if len(population_str) == 2:
                    city_info['Population'] = int(population_str[1])
            elif line.startswith('Like:'):
                like_str = line.split(': ')
                if len(like_str) == 2:
                    city_info['Like'] = int(like_str[1])
                    cities_info.append(city_info)
                    city_info = {}

    return cities_info

    return cities_info

def update_file_with_data(filename, new_data):
    # Convert the dictionary data into string format
    new_lines = []
    for city_info in new_data:
        name = city_info.get('Name', 'Unknown')
        coordinates = city_info.get('Coordinates', '')
        population = city_info.get('Population', 0)
        like = city_info.get('Like', 0)
        new_lines.append(f"Name: {name}\n")
        new_lines.append(f"Coordinates: {coordinates}\n")
        new_lines.append(f"Population: {population}\n")
        new_lines.append(f"Like: {like}\n\n")

    # Write the new data to the file
    with open(filename, 'w') as file:
        file.writelines(new_lines)

def smash_or_pass_launch(width, height, cities_info):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Smash or Pass Game")
    font = pygame.font.Font(None, 36)  # None indicates default font
    
    # Load like and X button images
    like_button = pygame.image.load("like.png")
    x_button = pygame.image.load("x_button.png")
    
    # Scale buttons to desired size
    button_size = (130, 130)
    like_button = pygame.transform.scale(like_button, button_size)
    x_button = pygame.transform.scale(x_button, button_size)

    # Calculate button positions
    space_between_buttons = 300
    total_button_height = max(like_button.get_height(), x_button.get_height())
    button_y = (height - total_button_height) // 1.2
    total_button_width = like_button.get_width() + space_between_buttons + x_button.get_width()
    button_x = (width - total_button_width) // 2
    
    # Position the buttons
    like_button_rect = like_button.get_rect(midbottom=(button_x + like_button.get_width() // 2, button_y + total_button_height))
    x_button_rect = x_button.get_rect(midbottom=(button_x + like_button.get_width() + space_between_buttons + x_button.get_width() // 2, button_y + total_button_height))
    
    random_city = random.choice(cities_info)
    while True:
        print("City:", random_city.get('Name', 'N/A'))
        print("Population:", random_city.get('Population', 'N/A'))
        print("Coordinates:", random_city.get('Coordinates', 'N/A'))
        print("Like:", random_city.get('Like', 'N/A'))
        print()  # Print an empty line for separation
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if like_button_rect.collidepoint(mouse_pos):
                        random_city['Like'] += 1
                        update_file_with_data("cities_info.txt", cities_info)
                        random_city = random.choice(cities_info)
                        print("Smash")
                    elif x_button_rect.collidepoint(mouse_pos):
                        random_city = random.choice(cities_info)
                        print("Pass")
        
        screen.fill((255, 255, 255))  # Fill the screen with white color
        
        # Display buttons at their positions
        screen.blit(like_button, like_button_rect)
        screen.blit(x_button, x_button_rect)
        
        pygame.display.update()

if __name__ == "__main__":
    smash_or_pass_launch(600, 800, read_file_info("cities_info.txt"))
