import pygame
import sys
from menu import run_menu, run_level_select
from game import run_game

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Project")
#asadh
# Mely pályák vannak teljesítve
completed_levels = {1: False, 2: False, 3: False}

state = "menu"
selected_level = None
running = True

while running:
    if state == "menu":
        result = run_menu(screen)
        if result == "exit":
            running = False
        elif result == "level_select":
            state = "level_select"

    elif state == "level_select":
        selected_level = run_level_select(screen, completed_levels)
        if selected_level == "back":
            state = "menu"
        elif selected_level in [1, 2, 3]:
            state = "game"

    elif state == "game":
        result = run_game(screen, selected_level)

        if result == "win":
            completed_levels[selected_level] = True
            state = "menu"

        elif result == "menu":
            state = "menu"

        elif result == "exit":
            running = False

pygame.quit()
sys.exit()
