import pygame
import time
WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 40
def load_level(n):
   with open(f"level{n}.txt", "r") as f:
       return [line.rstrip("\n") for line in f]
def is_on_ground(player, blocks):
   t = player.copy()
   t.y += 1
   for b in blocks:
       if t.colliderect(b):
           return True
   return False
def run_game(screen, level_number):
   clock = pygame.time.Clock()
   level = load_level(level_number)
   blocks = []
   checkpoints = []
   player = None
   goal = None
   enemy = None
   player_y_vel = 0
   for y, row in enumerate(level):
       for x, char in enumerate(row):
           if char == "#":
               blocks.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
           elif char == "P":
               player = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 40, 40)
           elif char == "G":
               goal = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
           elif char == "E":
               enemy = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + 10, 30, 30)
           elif char == "C":
               checkpoints.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
   gravity = 0.6
   jump_strength = -13
   move_speed = 5
   running = True
   while running:
       keys = pygame.key.get_pressed()
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               return "exit"
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   return "menu"
               if event.key == pygame.K_SPACE:
                   if is_on_ground(player, blocks):
                       player_y_vel = jump_strength
       dx = 0
       if keys[pygame.K_LEFT]:
           dx = -move_speed
       if keys[pygame.K_RIGHT]:
           dx = move_speed
       player.x += dx
       for b in blocks:
           if player.colliderect(b):
               if dx > 0:
                   player.right = b.left
               if dx < 0:
                   player.left = b.right
       player_y_vel += gravity
       player.y += int(player_y_vel)
       for b in blocks:
           if player.colliderect(b):
               if player_y_vel > 0:
                   player.bottom = b.top
                   player_y_vel = 0
               elif player_y_vel < 0:
                   player.top = b.bottom
                   player_y_vel = 0
       if player.x < 0:
           player.x = 0
       if player.right > WIDTH:
           player.right = WIDTH
       if player.colliderect(goal):
           font = pygame.font.SysFont(None, 100)
           text = font.render("WIN", True, (0, 255, 0))
           screen.fill((0, 0, 0))
           screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
           pygame.display.flip()
           time.sleep(2)
           return "menu"
       screen.fill((135, 206, 235))
       for b in blocks:
           pygame.draw.rect(screen, (0, 0, 0), b)
       for c in checkpoints:
           pygame.draw.rect(screen, (255, 255, 0), c)
       pygame.draw.rect(screen, (255, 0, 0), player)
       pygame.draw.rect(screen, (0, 255, 0), goal)
       if enemy:
           pygame.draw.rect(screen, (0, 0, 255), enemy)
       pygame.display.flip()
       clock.tick(60)
   return "menu"