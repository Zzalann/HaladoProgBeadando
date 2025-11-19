import pygame
import sys
from menu import run_menu
from game import run_game
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Project")
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
       from menu import run_level_select
       selected_level = run_level_select(screen)
       if selected_level == "back":
           state = "menu"
       elif selected_level in [1,2,3]:
           state = "game"
   elif state == "game":
       r = run_game(screen, selected_level)
       if r == "menu":
           state = "menu"
       elif r == "exit":
           running = False
pygame.quit()
sys.exit()