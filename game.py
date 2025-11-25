import pygame
import time
import random
import math

WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 40

# ---------------------------------------------------
# SPRITE BETÖLTÉS
# ---------------------------------------------------

player_img_right = pygame.transform.scale(pygame.image.load("sprites/player.png"), (40, 40))
player_img_left = pygame.transform.flip(player_img_right, True, False)

enemy_img = pygame.transform.scale(pygame.image.load("sprites/enemy.png"), (40, 40))
block_img = pygame.transform.scale(pygame.image.load("sprites/block.png"), (40, 40))
lava_img = pygame.transform.scale(pygame.image.load("sprites/lava.png"), (40, 40))
checkpoint_img = pygame.transform.scale(pygame.image.load("sprites/checkpoint.png"), (40, 40))
goal_img = pygame.transform.scale(pygame.image.load("sprites/goal.png"), (40, 40))

background_img = pygame.image.load("backgrounds/bg1.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# ---------------------------------------------------

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

def move_towards(enemy_rect, target_rect, speed):
    dx = target_rect.x - enemy_rect.x
    dy = target_rect.y - enemy_rect.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 0, 0
    return (dx / dist) * speed, (dy / dist) * speed

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------

def draw_button(screen, text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.x + 10, rect.y + 10))

def run_quiz(screen, level_number):
    if level_number == 1:
        questions = [
            ["Milyen színű a fű?", ["Kék", "Zöld", "Piros", "Fehér"], 1],
            ["Mennyi 2*5?", ["7", "9", "10", "12"], 2],
            ["Milyen színű a nap?", ["Lila", "Narancssárga", "Fekete", "Zöld"], 1],
            ["Melyik a legkisebb?", ["5", "2", "9", "1"], 3],
            ["Mennyi 3+4?", ["5", "6", "7", "8"], 2],
        ]
    elif level_number == 2:
        questions = [
            ["Melyik év szökőév?", ["2023", "2024", "2025", "2026"], 1],
            ["Milyen színű a vér?", ["Zöld", "Kék", "Piros", "Sárga"], 2],
            ["Mennyi 10/2?", ["4", "5", "6", "8"], 1],
            ["Melyik a legnagyobb?", ["3", "12", "7", "9"], 1],
            ["Milyen színű a hó?", ["Fehér", "Fekete", "Zöld", "Piros"], 0],
        ]
    else:
        questions = [
            ["Mennyi 6+6?", ["10", "11", "12", "14"], 2],
            ["Milyen színű a tenger?", ["Piros", "Sárga", "Kék", "Lila"], 2],
            ["Mennyi 15-5?", ["5", "10", "15", "20"], 1],
            ["Melyik igaz?", ["A víz szilárd", "A tűz hideg", "A Nap csillag", "A Hold csillag"], 2],
            ["Melyik a legkisebb?", ["20", "8", "3", "14"], 2],
        ]

    question = random.choice(questions)
    q_text, answers, correct = question

    btns = [
        pygame.Rect(300, 250, 400, 50),
        pygame.Rect(300, 320, 400, 50),
        pygame.Rect(300, 390, 400, 50),
        pygame.Rect(300, 460, 400, 50),
    ]
    give_up = pygame.Rect(10, 10, 200, 50)

    while True:
        screen.fill((20, 20, 20))
        font = pygame.font.SysFont(None, 50)
        t = font.render(q_text, True, (255, 255, 255))
        screen.blit(t, (50, 100))

        for i in range(4):
            draw_button(screen, answers[i], btns[i], (70, 70, 70), (255, 255, 255))

        draw_button(screen, "Feladom", give_up, (180, 0, 0), (255, 255, 255))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if give_up.collidepoint(mx, my):
                    return "menu"

                for i in range(4):
                    if btns[i].collidepoint(mx, my):
                        if i == correct:
                            return "correct"
                        else:
                            return "wrong"

# ---------------------------------------------------
# JÁTÉK LOGIKA + AI + SPRITE + MOZGÓ PLATFORM
# ---------------------------------------------------

def run_game(screen, level_number):
    clock = pygame.time.Clock()

    while True:
        level = load_level(level_number)

        blocks = []
        lava = []
        checkpoints = []
        moving_blocks = []
        player = None
        goal = None
        enemy = None

        player_y_vel = 0
        player_direction = "right"
        checkpoint_done = False

        # --- pálya beolvasás ---
        for y, row in enumerate(level):
            for x, char in enumerate(row):
                tile = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)

                if char == "#":
                    blocks.append(tile)
                elif char == "L":
                    lava.append(tile)
                elif char == "P":
                    player = tile
                elif char == "G":
                    goal = tile
                elif char == "C":
                    checkpoints.append(tile)
                elif char == "E":
                    enemy = tile
                    enemy_home = tile.copy()
                    enemy_state = "idle"
                elif char == "M":
                    rect = tile
                    moving_blocks.append({
                        "rect": rect,
                        "speed": 2,
                        "min_x": rect.x - 80,
                        "max_x": rect.x + 80
                    })

        exit_btn = pygame.Rect(950, 10, 40, 40)

        # ---------------------------------------------------
        # JÁTÉK FŐ CIKLUS
        # ---------------------------------------------------
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_btn.collidepoint(event.pos):
                        return "menu"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_SPACE:
                        all_ground = blocks + [mb["rect"] for mb in moving_blocks]
                        if is_on_ground(player, all_ground):
                            player_y_vel = -13

            # ------------------ PLAYER MOZGÁS ------------------

            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -5
                player_direction = "left"
            if keys[pygame.K_RIGHT]:
                dx = 5
                player_direction = "right"

            player.x += dx

            # ütközés falakkal (X irányban)
            for b in blocks:
                if player.colliderect(b):
                    if dx > 0:
                        player.right = b.left
                    elif dx < 0:
                        player.left = b.right

            # mozgó platformok X irányú mozgatása
            for mb in moving_blocks:
                r = mb["rect"]
                r.x += mb["speed"]
                if r.x < mb["min_x"] or r.x > mb["max_x"]:
                    mb["speed"] *= -1

            # gravitáció
            player_y_vel += 0.6
            player.y += int(player_y_vel)

            # ütközés falakkal (Y irányban)
            for b in blocks:
                if player.colliderect(b):
                    if player_y_vel > 0:
                        player.bottom = b.top
                    elif player_y_vel < 0:
                        player.top = b.bottom
                    player_y_vel = 0

            # ütközés mozgó platformokkal (Y irányban + "viszi" a playert)
            for mb in moving_blocks:
                r = mb["rect"]
                if player.colliderect(r):
                    if player_y_vel > 0:
                        player.bottom = r.top
                        player_y_vel = 0
                        player.x += mb["speed"]
                    elif player_y_vel < 0:
                        player.top = r.bottom
                        player_y_vel = 0

            # ------------------ ENEMY AI ------------------

            if enemy:
                dist = abs(enemy.x - player.x)

                if dist < 200:
                    enemy_state = "chase"

                elif enemy_state == "chase" and dist >= 200:
                    enemy_state = "return"

                if enemy_state == "chase":
                    vx, vy = move_towards(enemy, player, 2)
                    enemy.x += vx
                    enemy.y += vy

                elif enemy_state == "return":
                    vx, vy = move_towards(enemy, enemy_home, 2)
                    enemy.x += vx
                    enemy.y += vy

                    if abs(enemy.x - enemy_home.x) < 3:
                        enemy_state = "idle"

            # ------------------ HALÁL ELLENŐRZÉS ------------------

            if enemy and enemy.colliderect(player):
                return "game_over"

            for lv in lava:
                if player.colliderect(lv):
                    return "game_over"

            # ------------------ GOAL ------------------

            if player.colliderect(goal):
                if not checkpoint_done:
                    pass  # player tovább mehet, csak még nem nyerhet
                else:
                    return "win"

            # ------------------ CHECKPOINT ------------------

            if not checkpoint_done:
                for c in checkpoints:
                    if player.colliderect(c):
                        result = run_quiz(screen, level_number)
                        if result == "correct":
                            checkpoint_done = True
                        elif result == "wrong":
                            return "game_over"
                        else:
                            return "menu"

            # ------------------ KÉPERNYŐ RAJZOLÁSA ------------------

            screen.blit(background_img, (0, 0))

            # pálya sprite-ok
            for b in blocks:
                screen.blit(block_img, (b.x, b.y))
            for lv in lava:
                screen.blit(lava_img, (lv.x, lv.y))
            for c in checkpoints:
                screen.blit(checkpoint_img, (c.x, c.y))

            # mozgó platformok kirajzolása
            for mb in moving_blocks:
                r = mb["rect"]
                screen.blit(block_img, (r.x, r.y))

            # enemy
            if enemy:
                screen.blit(enemy_img, (enemy.x, enemy.y))

            # goal
            screen.blit(goal_img, (goal.x, goal.y))

            # player sprite
            if player_direction == "right":
                screen.blit(player_img_right, (player.x, player.y))
            else:
                screen.blit(player_img_left, (player.x, player.y))

            # exit button
            pygame.draw.rect(screen, (255, 0, 0), exit_btn)
            pygame.draw.line(screen, (255, 255, 255), (955, 15), (985, 45), 4)
            pygame.draw.line(screen, (255, 255, 255), (985, 15), (955, 45), 4)

            pygame.display.flip()
            clock.tick(60)
