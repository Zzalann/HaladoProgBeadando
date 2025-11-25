import pygame
import sys
from menu import run_menu, run_level_select, run_game_over, run_win_screen
from game import run_game

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Project")

# Minden pálya alapból zárva (kivéve az első)
completed_levels = {1: False, 2: False, 3: False}

state = "menu"
selected_level = None
running = True

while running:

    # ────────────────────────────────────────────────
    # FŐMENÜ
    # ────────────────────────────────────────────────
    if state == "menu":
        result = run_menu(screen)
        if result == "exit":
            running = False
        elif result == "level_select":
            state = "level_select"

    # ────────────────────────────────────────────────
    # PÁLYAVÁLASZTÓ
    # ────────────────────────────────────────────────
    elif state == "level_select":
        selected_level = run_level_select(screen, completed_levels)

        if selected_level == "back":
            state = "menu"

        # 1. pálya mindig indítható
        elif selected_level == 1:
            state = "game"

        # 2. és 3. csak a megelőző pálya teljesítése után
        elif selected_level == 2 and completed_levels[1]:
            state = "game"

        elif selected_level == 3 and completed_levels[2]:
            state = "game"


    # ────────────────────────────────────────────────
    # JÁTÉK
    # ────────────────────────────────────────────────
    elif state == "game":
        result = run_game(screen, selected_level)

        if result == "win":
            completed_levels[selected_level] = True
            state = "win_screen"

        elif result == "menu":
            state = "menu"

        elif result == "game_over":
            state = "game_over"

        elif result == "exit":
            running = False

    # ────────────────────────────────────────────────
    # WIN SCREEN
    # ────────────────────────────────────────────────
    elif state == "win_screen":
        result = run_win_screen(screen)

        if result == "menu":
            state = "level_select"

        elif result == "exit":
            running = False

    # ────────────────────────────────────────────────
    # GAME OVER SCREEN
    # ────────────────────────────────────────────────
    elif state == "game_over":
        result = run_game_over(screen)

        if result == "retry":
            state = "game"

        elif result == "menu":
            state = "level_select"

        elif result == "exit":
            running = False

pygame.quit()
sys.exit()
