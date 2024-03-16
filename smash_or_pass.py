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
        screen.blit(x_button, x_button_rect)
        
        pygame.display.update()

if __name__ == "__main__":
    smash_or_pass_launch(800, 1000)