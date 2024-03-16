#!/usr/bin/env python3

import pygame
import sys
import random
import json
import requests

def save_city_data(data):
    with open('city_data.json', 'w') as file:
        json.dump(data, file, indent=4)

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
        data_filter = [data['results'][index] for index in range(0, len(data['results'])) if ' ' not in data['results'][index]['name']]
        return data_filter

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
    x_button_rect = like_button.get_rect(midbottom=(button_x + like_button.get_width() // 2, button_y + total_button_height))
    like_button_rect = x_button.get_rect(midbottom=(button_x + like_button.get_width() + space_between_buttons + x_button.get_width() // 2, button_y + total_button_height))
    
    # Main loop
    random_city = cities_info[random.randint(0, len(cities_info) - 1)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if like_button_rect.collidepoint(mouse_pos):
                        random_city = cities_info[random.randint(0, len(cities_info) - 1)]
                    elif x_button_rect.collidepoint(mouse_pos):
                        random_city = cities_info[random.randint(0, len(cities_info) - 1)]
        
        screen.fill((255, 255, 255))  # Fill the screen with white color
        
        # Display buttons at their positions
        screen.blit(like_button, like_button_rect)
        screen.blit(x_button, x_button_rect)
        
        # Display the name of the city at the middle-top of the window
        city_name_text = font.render(random_city['name'], True, (0, 0, 0))
        city_name_rect = city_name_text.get_rect(center=(width // 2, height // 10))
        screen.blit(city_name_text, city_name_rect)
        
        pygame.display.update()

if __name__ == "__main__":
    smash_or_pass_launch(600, 800, get_random_city())
