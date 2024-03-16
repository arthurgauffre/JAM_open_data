#!/usr/bin/env python3

import subprocess
import pygame
import sys
import random
import requests
import os
import re

def download_image(url, filename):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        images_folder = 'images/'

        filepath = os.path.join(images_folder, filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)

        print(f"Image downloaded successfully as {filepath}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_image_content(filename):
    try:
        filepath = os.path.join('images/', filename)

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r'<meta property="og:image" content="(.+?)">'
        match = re.search(pattern, content)

        if match:
            return match.group(1)
        else:
            return "No meta tag found in the file."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def remove_file_from_images(filename):
    try:
        filepath = os.path.join('images/', filename)

        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"File '{filename}' removed successfully from /images folder.")
        else:
            print(f"File '{filename}' does not exist in /images folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_image_url(article_title):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get("https://en.wikipedia.org/w/api.php", 
                            params={"action": "parse", 
                                    "page": article_title,
                                    "format": "json"},
                            headers=headers)
    data = response.json()
    image_url = "https://upload.wikimedia.org/wikipedia/commons/6/6c/No_image_3x4.svg"
    
    if "images" in data["parse"]:
        for image in data["parse"]["images"]:
            if image.lower().endswith(".jpg"):
                image_url = f"https://en.wikipedia.org/wiki/File:{image}"
                break
    if image_url == "https://upload.wikimedia.org/wikipedia/commons/6/6c/No_image_3x4.svg":
        download_image(image_url, "current_image.jpg")
        return image_url
    download_image(image_url, f"{article_title}.txt")
    image_url = get_image_content(f"{article_title}.txt")
    download_image(image_url, "current_image.jpg")
    remove_file_from_images(f"{article_title}.txt")
    return image_url

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
    like_button = pygame.image.load("images/like.png")
    x_button = pygame.image.load("images/x_button.png")

    # load image logo
    logo = pygame.image.load("images/logo.png")
    logo = pygame.transform.scale(logo, (300, 150))

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
    lines = []
    current_line = ""
    # for word in city_description.split():
    #     test_line = current_line + word + " "
    #     if font.size(test_line)[0] < width:  # Vérifie si le mot peut être ajouté à la ligne
    #         current_line = test_line
    #     else:  # Si la ligne dépasse la largeur de l'écran, ajoutez-la à la liste des lignes et commencez une nouvelle ligne
    #         lines.append(current_line)
    #         current_line = word + " "
    # lines.append(current_line)
    # city_description_surface = [font.render(line, True, (0, 0, 0)) for line in lines]
    y_pos = 0  # Position of the first line

    get_image_url("Poitiers")
    image = pygame.image.load("images/current_image.jpg")
    image = pygame.transform.scale(image, (500, 300))

    while True:
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
                        remove_file_from_images("current_image.jpg")
                    elif x_button_rect.collidepoint(mouse_pos):
                        random_city = random.choice(cities_info)
        
        screen.fill((255, 255, 255))  # Fill the screen with white color
        
        screen.blit(image, (width // 2 - 250, 200))
        # Display buttons at their positions
        screen.blit(like_button, like_button_rect)

        logo_rect = logo.get_rect(center=(width // 2, 100))
        screen.blit(logo, logo_rect)

        # Display city description
        # for text_surface in city_description_surface:
        #     text_rect = text_surface.get_rect(midtop=(width // 2, y_pos))
        #     screen.blit(text_surface, text_rect)
        #     y_pos += text_surface.get_height()

        # Display X button at the bottom left corner
        x_button_rect = x_button.get_rect(bottomleft=(20, height - 20))
        screen.blit(x_button, x_button_rect)
        
        pygame.display.update()

if __name__ == "__main__":
    get_image_url("Poitiers")
    smash_or_pass_launch(600, 800, read_file_info("cities_info.txt"))
