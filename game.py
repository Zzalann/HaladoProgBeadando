import pygame
import time
import random
import os

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

def draw_button(screen, text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.x + 20, rect.y + 15))

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
            draw_button(screen, answers[i], btns[i], (50, 50, 50), (255, 255, 255))

        draw_button(screen, "Feladom", give_up, (200, 0, 0), (255, 255, 255))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
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

def run_game(screen, level_number):
    clock = pygame.time.Clock()

    # --- SPRITE BETÖLTÉS ---
    player_img = pygame.image.load("sprites/player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (40, 40))

    enemy_img = pygame.image.load("sprites/enemy.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (40, 40))

    block_img = pygame.image.load("sprites/block.png").convert_alpha()
    block_img = pygame.transform.scale(block_img, (40, 40))

    checkpoint_img = pygame.image.load("sprites/checkpoint.png").convert_alpha()
    checkpoint_img = pygame.transform.scale(checkpoint_img, (40, 40))

    goal_img = pygame.image.load("sprites/goal.png").convert_alpha()
    goal_img = pygame.transform.scale(goal_img, (40, 40))

    bg_img = pygame.image.load("backgrounds/bg1.png").convert()
    bg_img = pygame.transform.scale(bg_img, (1000, 600))
    while True:
        level = load_level(level_number)

        blocks = []
        checkpoints = []
        player = None
        goal = None
        enemy = None
        player_y_vel = 0
        checkpoint_done = False
        message_text = ""
        message_time = 0

        # Pálya beolvasása
        for y, row in enumerate(level):
            for x, char in enumerate(row):
                if char == "#":
                    blocks.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == "P":
                    player = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)
                elif char == "G":
                    goal = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                elif char == "E":
                    enemy = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 30, 30)
                elif char == "C":
                    checkpoints.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        exit_btn = pygame.Rect(950, 10, 40, 40)

        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_SPACE and is_on_ground(player, blocks):
                        player_y_vel = -13
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_btn.collidepoint(event.pos):
                        return "menu"

            # Mozgás
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -5
            if keys[pygame.K_RIGHT]:
                dx = 5

            player.x += dx
            for b in blocks:
                if player.colliderect(b):
                    if dx > 0:
                        player.right = b.left
                    elif dx < 0:
                        player.left = b.right

            player_y_vel += 0.6
            player.y += int(player_y_vel)

            for b in blocks:
                if player.colliderect(b):
                    if player_y_vel > 0:
                        player.bottom = b.top
                        player_y_vel = 0
                    elif player_y_vel < 0:
                        player.top = b.bottom
                        player_y_vel = 0

            # WIN
            if player.colliderect(goal):
                if not checkpoint_done:
                    message_text = "MENJ A CHECKPOINTHOZ!"
                    message_time = pygame.time.get_ticks() + 1500
                else:
                    screen.fill((0,0,0))
                    f = pygame.font.SysFont(None, 100)
                    t = f.render("WIN", True, (0,255,0))
                    screen.blit(t, (400,250))
                    pygame.display.flip()
                    time.sleep(2)
                    return "menu"

            # CHECKPOINT
            if not checkpoint_done:
                for c in checkpoints:
                    if player.colliderect(c):
                        result = run_quiz(screen, level_number)

                        if result == "correct":
                            checkpoint_done = True
                            message_text = "HELYES VÁLASZ!"
                            message_time = pygame.time.get_ticks() + 1200

                        elif result == "wrong":
                            return "restart"
                        else:
                            return "menu"

            # RAJZOLÁS
            screen.blit(bg_img, (0,0))

            for b in blocks:
                screen.blit(block_img, (b.x, b.y))
            for cc in checkpoints:
                screen.blit(checkpoint_img, (cc.x, cc.y))

            screen.blit(player_img, (player.x, player.y))
            if enemy:
                screen.blit(enemy_img, (enemy.x, enemy.y))
            screen.blit(goal_img, (goal.x, goal.y))

            pygame.draw.rect(screen, (255,0,0), exit_btn)
            pygame.draw.line(screen, (255,255,255), (955,15), (985,45), 4)
            pygame.draw.line(screen, (255,255,255), (985,15), (955,45), 4)

            if message_text and pygame.time.get_ticks() < message_time:
                font = pygame.font.SysFont(None, 40)
                msg = font.render(message_text, True, (0,255,0))
                screen.blit(msg, (WIDTH//2 - 180, 20))

            pygame.display.flip()
            clock.tick(60)
