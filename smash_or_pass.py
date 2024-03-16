#!/usr/bin/env python3

import subprocess
import pygame
import sys

def generate_city_description(city_name):
    prompt = f"créer une description de max 200 caractères sur la ville de {city_name}."
    command_output = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True).stdout.decode('utf-8')
    return command_output

def smash_or_pass_launch(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Smash or Pass Game")
    font = pygame.font.Font(None, 36)  # None indicates default font
    
    # Load like and X button images
    like_button = pygame.image.load("like.png")
    x_button = pygame.image.load("x_button.png")

    # load image logo
    logo = pygame.image.load("logo.png")
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
    
    # Add text description of the city
    city_name = "Paris"
    city_description = "La vie est un voyage imprévisible. Faisons de chaque instant une aventure. Apprécions les petits bonheurs et embrassons les défis avec courage."
    lines = []
    current_line = ""
    for word in city_description.split():
        test_line = current_line + word + " "
        if font.size(test_line)[0] < width:  # Vérifie si le mot peut être ajouté à la ligne
            current_line = test_line
        else:  # Si la ligne dépasse la largeur de l'écran, ajoutez-la à la liste des lignes et commencez une nouvelle ligne
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    city_description_surface = [font.render(line, True, (0, 0, 0)) for line in lines]
    y_pos = 0  # Position of the first line

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if like_button_rect.collidepoint(mouse_pos):
                        print("Smash")
                    elif x_button_rect.collidepoint(mouse_pos):
                        print("Pass")
        
        screen.fill((255, 255, 255))  # Fill the screen with white color
        
        # Display buttons at their positions
        screen.blit(like_button, like_button_rect)

        logo_rect = logo.get_rect(center=(width // 2, 100))
        screen.blit(logo, logo_rect)

        # Display city description
        for text_surface in city_description_surface:
            text_rect = text_surface.get_rect(midtop=(width // 2, y_pos))
            screen.blit(text_surface, text_rect)
            y_pos += text_surface.get_height()

        # Display X button at the bottom left corner
        x_button_rect = x_button.get_rect(bottomleft=(20, height - 20))
        screen.blit(x_button, x_button_rect)
        
        pygame.display.update()

if __name__ == "__main__":
    smash_or_pass_launch(800, 1000)