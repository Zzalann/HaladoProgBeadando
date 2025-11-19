import pygame
import time
import os
import random

WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 40


# SPRITE BETÖLTŐ 

def load_sprite(path, size):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

# PÁLYA BETÖLTÉSE

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


# GOMB

def draw_button(screen, text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (255,255,255), rect, 3, border_radius=10)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.x + (rect.width - t.get_width())//2,
                    rect.y + (rect.height - t.get_height())//2))


# KVÍZ

def run_quiz(screen, level_number):

    if level_number == 1:
        questions = [
            ["Milyen színű a fű?", ["Kék", "Zöld", "Piros", "Fehér"], 1],
            ["Mennyi 2*5?", ["7", "9", "10", "11"], 2],
        ]

    elif level_number == 2:
        questions = [
            ["Melyik év szökőév?", ["2023", "2024", "2025", "2026"], 1],
            ["Milyen színű a vér?", ["Zöld", "Kék", "Piros", "Sárga"], 2],
        ]

    else:
        questions = [
            ["Mennyi 6+6?", ["10", "11", "12", "14"], 2],
            ["Milyen színű a tenger?", ["Piros", "Sárga", "Kék", "Lila"], 2],
        ]

    q_text, answers, correct = random.choice(questions)
    btns = [pygame.Rect(300, 260 + i*70, 400, 60) for i in range(4)]
    exit_btn = pygame.Rect(10, 10, 200, 50)

    clock = pygame.time.Clock()

    while True:
        screen.fill((20,20,20))

        font = pygame.font.SysFont(None, 45)
        t = font.render(q_text, True, (255,255,255))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 120))

        for i in range(4):
            draw_button(screen, answers[i], btns[i], (50,50,50), (255,255,255))

        draw_button(screen, "Feladom", exit_btn, (200,0,0), (255,255,255))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_btn.collidepoint(event.pos):
                    return "menu"
                for i in range(4):
                    if btns[i].collidepoint(event.pos):
                        return "correct" if i == correct else "wrong"


# A JÁTÉK

def run_game(screen, level_number):

    clock = pygame.time.Clock()

    # SPRITEOK 
    player_img = load_sprite("sprites/player.png", (40,40))
    enemy_img = load_sprite("sprites/enemy.png", (40,40))
    block_img = load_sprite("sprites/block.png", (40,40))
    checkpoint_img = load_sprite("sprites/checkpoint.png", (40,40))
    goal_img = load_sprite("sprites/goal.png", (40,40))
    bg_img = pygame.image.load("backgrounds/bg1.png").convert()

    # PÁLYA BEOLVASÁS
    level = load_level(level_number)
    blocks = []
    checkpoints = []
    player = None
    enemy = None
    goal = None

    for y, row in enumerate(level):
        for x, ch in enumerate(row):
            if ch == "#":
                blocks.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif ch == "P":
                player = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)
            elif ch == "G":
                goal = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)
            elif ch == "E":
                enemy = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE+10, 40, 40)
            elif ch == "C":
                checkpoints.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40))

    player_y_vel = 0
    checkpoint_done = False

    message_text = ""
    msg_timer = 0

    exit_btn = pygame.Rect(950, 10, 40, 40)

    # GAME LOOP 
    while True:

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_SPACE and is_on_ground(player, blocks):
                    player_y_vel = -15  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_btn.collidepoint(event.pos):
                    return "menu"

        # MOZGÁS
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        player.x += dx

        for b in blocks:
            if player.colliderect(b):
                if dx > 0: player.right = b.left
                if dx < 0: player.left = b.right

        # GRAVITÁCIÓ
        player_y_vel += 0.6
        player.y += int(player_y_vel)

        for b in blocks:
            if player.colliderect(b):
                if player_y_vel > 0:
                    player.bottom = b.top
                    player_y_vel = 0
                else:
                    player.top = b.bottom
                    player_y_vel = 0

        # WIN
        if player.colliderect(goal):
            if not checkpoint_done:
                message_text = "MENJ A CHECKPOINTHOZ!"
                msg_timer = pygame.time.get_ticks() + 1500
            else:
                return "win"

        # CHECKPOINT LOGIKA
        if not checkpoint_done:
            for c in checkpoints:
                if player.colliderect(c):
                    result = run_quiz(screen, level_number)
                    if result == "correct":
                        checkpoint_done = True
                        message_text = "HELYES VÁLASZ!"
                        msg_timer = pygame.time.get_ticks() + 1200
                    else:
                        return "menu"

        # RAJZOLÁS 
        screen.blit(bg_img, (0,0))

        for b in blocks:
            screen.blit(block_img, (b.x, b.y))

        for c in checkpoints:
            screen.blit(checkpoint_img, (c.x, c.y))

        screen.blit(player_img, (player.x, player.y))

        if enemy:
            screen.blit(enemy_img, (enemy.x, enemy.y))

        screen.blit(goal_img, (goal.x, goal.y))

        # EXIT
        pygame.draw.rect(screen, (255,0,0), exit_btn)
        pygame.draw.line(screen, (255,255,255), (955,15),(985,45),3)
        pygame.draw.line(screen, (255,255,255), (985,15),(955,45),3)

        # ÜZENET
        if message_text and pygame.time.get_ticks() < msg_timer:
            font = pygame.font.SysFont(None, 40)
            t = font.render(message_text, True, (255,255,0))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 20))
        else:
            message_text = ""

        pygame.display.flip()
        clock.tick(60)
