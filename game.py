import pygame
import time
import os
import random

WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 40

# ------------------------------------------------------
# SPRITE BETÖLTŐ
# ------------------------------------------------------
def load_sprite(path, size):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

# ------------------------------------------------------
# LEVEL BETÖLTÉS
# ------------------------------------------------------
def load_level(n):
    with open(f"level{n}.txt", "r") as f:
        return [line.rstrip("\n") for line in f]

def is_on_ground(player, blocks, moving_blocks):
    t = player.copy()
    t.y += 1

    for b in blocks:
        if t.colliderect(b):
            return True
    for mb in moving_blocks:
        if t.colliderect(mb["rect"]):
            return True
    return False

# ------------------------------------------------------
# KVÍZ
# ------------------------------------------------------
def run_quiz(screen, level_number):

    questions = {
        1: [
            ["Milyen színű a fű?", ["Kék","Zöld","Piros","Fehér"], 1],
            ["Mennyi 2*5?", ["7","9","10","11"], 2],
        ],
        2: [
            ["Melyik év szökőév?", ["2023","2024","2025","2026"], 1],
            ["Milyen színű a vér?", ["Zöld","Kék","Piros","Sárga"], 2],
        ],
        3: [
            ["Mennyi 6+6?", ["10","11","12","14"], 2],
            ["Milyen színű a tenger?", ["Piros","Sárga","Kék","Lila"], 2],
        ]
    }

    q_text, answers, correct = random.choice(questions[level_number])

    btns = [pygame.Rect(300, 260 + i*70, 400, 60) for i in range(4)]
    exit_btn = pygame.Rect(10, 10, 200, 50)
    clock = pygame.time.Clock()

    while True:
        screen.fill((20,20,20))

        font = pygame.font.SysFont(None, 45)
        t = font.render(q_text, True, (255,255,255))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 120))

        for i in range(4):
            pygame.draw.rect(screen, (80,80,80), btns[i], border_radius=10)
            font = pygame.font.SysFont(None, 40)
            text = font.render(answers[i], True, (255,255,255))
            screen.blit(text, (btns[i].x + 20, btns[i].y + 10))

        pygame.draw.rect(screen, (200,0,0), exit_btn)
        font = pygame.font.SysFont(None, 40)
        t = font.render("Feladom", True, (255,255,255))
        screen.blit(t, (20, 20))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if exit_btn.collidepoint((mx,my)):
                    return "menu"

                for i in range(4):
                    if btns[i].collidepoint((mx,my)):
                        return "correct" if i == correct else "wrong"

# ------------------------------------------------------
# FŐ JÁTÉK
# ------------------------------------------------------
def run_game(screen, level_number):

    clock = pygame.time.Clock()

    # ---- SPRITES ----
    player_img = load_sprite("sprites/player.png", (40,40))
    player_img_left = pygame.transform.flip(player_img, True, False)
    facing_left = False

    enemy_img = load_sprite("sprites/enemy.png", (40,40))
    block_img = load_sprite("sprites/block.png", (40,40))
    block2_img = load_sprite("sprites/block2.png", (40,40))
    checkpoint_img = load_sprite("sprites/checkpoint.png", (40,40))
    goal_img = load_sprite("sprites/goal.png", (40,40))
    lava_img = load_sprite("sprites/lava.png", (40,40))
    bg_img = pygame.image.load("backgrounds/bg1.png").convert()

    # ---- LEVEL BEOLVASÁS ----
    level = load_level(level_number)
    blocks = []
    moving_blocks = []
    lava_blocks = []
    checkpoints = []
    player = None
    enemy = None
    goal = None
    start_pos = None

    for y, row in enumerate(level):
        for x, ch in enumerate(row):

            if ch == "#":
                blocks.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

            elif ch == "M":
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                moving_blocks.append({
                    "rect": rect,
                    "speed": 2,
                    "min_x": rect.x - 80,
                    "max_x": rect.x + 80
                })

            elif ch == "L":
                lava_blocks.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

            elif ch == "P":
                player = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)
                start_pos = player.copy()

            elif ch == "G":
                goal = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)

            elif ch == "E":
                enemy = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)

            elif ch == "C":
                checkpoints.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40))

    player_y_vel = 0
    checkpoint_done = False
    exit_btn = pygame.Rect(950, 10, 40, 40)

    # ----------------------------------------------------
    # JÁTÉK LOOP
    # ----------------------------------------------------
    while True:
        keys = pygame.key.get_pressed()

        # események
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_SPACE and is_on_ground(player, blocks, moving_blocks):
                    player_y_vel = -12

        # ---- PLAYER X MOZGÁS ----
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        if dx < 0:
            facing_left = True
        elif dx > 0:
            facing_left = False

        player.x += dx

        # fal ütközés
        for b in blocks:
            if player.colliderect(b):
                if dx > 0: player.right = b.left
                if dx < 0: player.left = b.right

        # mozgó block ütközés
        for mb in moving_blocks:
            r = mb["rect"]
            if player.colliderect(r):
                if dx > 0: player.right = r.left
                if dx < 0: player.left = r.right

        # ---- GRAVITÁCIÓ ----
        player_y_vel += 0.6
        player.y += int(player_y_vel)

        # block ütközés Y
        for b in blocks:
            if player.colliderect(b):
                if player_y_vel > 0:
                    player.bottom = b.top
                    player_y_vel = 0
                else:
                    player.top = b.bottom
                    player_y_vel = 0

        # mozgó block Y
        for mb in moving_blocks:
            r = mb["rect"]
            if player.colliderect(r):
                if player_y_vel > 0:
                    player.bottom = r.top
                    player_y_vel = 0
                    player.x += mb["speed"]
                else:
                    player.top = r.bottom
                    player_y_vel = 0

        # ---- MOZGÓ BLOCK MOZGÁS ----
        for mb in moving_blocks:
            mb["rect"].x += mb["speed"]
            if mb["rect"].x < mb["min_x"] or mb["rect"].x > mb["max_x"]:
                mb["speed"] *= -1

        # ---- LAVA HALÁL (javított hitbox) ----
        for lv in lava_blocks:
            if player.colliderect(lv):
                player.topleft = start_pos.topleft   # restart
                return "menu"

        # ---- CHECKPOINT ----
        if not checkpoint_done:
            for c in checkpoints:
                if player.colliderect(c):
                    result = run_quiz(screen, level_number)

                    if result == "correct":
                        checkpoint_done = True
                    else:
                        player.topleft = start_pos.topleft
                        return "menu"

        # ---- WIN ----
        if player.colliderect(goal):
            if not checkpoint_done:
                pass
            else:
                return "win"

        # ---- RAJZ ----
        screen.blit(bg_img, (0,0))

        for b in blocks: screen.blit(block_img, (b.x, b.y))
        for lv in lava_blocks: screen.blit(lava_img, (lv.x, lv.y))
        for mb in moving_blocks: screen.blit(block2_img, (mb["rect"].x, mb["rect"].y))
        for c in checkpoints: screen.blit(checkpoint_img, (c.x, c.y))

        # player irány sprite
        if facing_left:
            screen.blit(player_img_left, (player.x, player.y))
        else:
            screen.blit(player_img, (player.x, player.y))

        if enemy: screen.blit(enemy_img, (enemy.x, enemy.y))
        screen.blit(goal_img, (goal.x, goal.y))

        pygame.display.flip()
        clock.tick(60)
