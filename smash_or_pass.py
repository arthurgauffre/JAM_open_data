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
    button_size = (50, 50)
    like_button = pygame.transform.scale(like_button, button_size)
    x_button = pygame.transform.scale(x_button, button_size)
    
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
        
        # Display like button at the bottom right corner
        like_button_rect = like_button.get_rect(bottomright=(width - 20, height - 20))
        screen.blit(like_button, like_button_rect)
        
        # Display X button at the bottom left corner
        x_button_rect = x_button.get_rect(bottomleft=(20, height - 20))
        screen.blit(x_button, x_button_rect)
        
        pygame.display.update()

if __name__ == "__main__":
    smash_or_pass_launch(600, 800)