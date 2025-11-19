import pygame
import time
import random

WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 40
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Project")
clock = pygame.time.Clock()

# ---------- Színek ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKY = (135, 206, 235)
BUTTON_HOVER = (70, 70, 70)

# ---------- Segédfüggvények ----------
def draw_button(screen, rect, text, base_color, hover_color, text_color):
    mx, my = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mx, my) else base_color
    pygame.draw.rect(screen, BLACK, rect.inflate(4, 4), border_radius=10)  # keret
    pygame.draw.rect(screen, color, rect, border_radius=10)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))

def draw_message(screen, text, color, y=50):
    font = pygame.font.SysFont(None, 50)
    t = font.render(text, True, color)
    screen.blit(t, (WIDTH//2 - t.get_width()//2, y))

# ---------- Szintek betöltése ----------
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

# ---------- Kvíz ----------
def run_quiz(screen, level_number):
    questions = {
        1: [
            ["Milyen szinű a fű?", ["Kék", "Zöld", "Piros", "Fehér"], 1],
            ["Mennyi 2*5?", ["7", "9", "10", "12"], 2],
        ],
        2: [
            ["Melyik év szökőév?", ["2023", "2024", "2025", "2026"], 1],
            ["Milyen színű a vér?", ["Zöld", "Kék", "Piros", "Sárga"], 2],
        ],
        3: [
            ["Mennyi 6+6?", ["10", "11", "12", "14"], 2],
            ["Milyen színű a tenger?", ["Piros", "Sárga", "Kék", "Lila"], 2],
        ],
    }
    question = random.choice(questions[level_number])
    q_text, answers, correct = question
    btns = [pygame.Rect(300, 250 + i*70, 400, 60) for i in range(4)]
    give_up = pygame.Rect(10, 10, 200, 50)

    while True:
        screen.fill(DARK_GRAY)
        draw_message(screen, q_text, WHITE, y=100)
        for i, rect in enumerate(btns):
            draw_button(screen, rect, answers[i], GRAY, BUTTON_HOVER, WHITE)
        draw_button(screen, give_up, "Feladom", RED, (255,50,50), WHITE)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if give_up.collidepoint(mx, my):
                    return "menu"
                for i, rect in enumerate(btns):
                    if rect.collidepoint(mx, my):
                        return "correct" if i == correct else "wrong"

# ---------- Game Over képernyő ----------
def run_game_over(screen):
    restart_btn = pygame.Rect(300, 250, 400, 60)
    menu_btn = pygame.Rect(300, 350, 400, 60)
    while True:
        screen.fill(BLACK)
        draw_message(screen, "GAME OVER", RED, y=100)
        draw_button(screen, restart_btn, "Újra próbálom", GRAY, BUTTON_HOVER, WHITE)
        draw_button(screen, menu_btn, "Vissza a menübe", GRAY, BUTTON_HOVER, WHITE)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if restart_btn.collidepoint(mx, my):
                    return "restart"
                if menu_btn.collidepoint(mx, my):
                    return "menu"

# ---------- Játék futtatása ----------
def run_game(screen, level_number):
    while True:
        level = load_level(level_number)
        blocks, checkpoints, player, goal, enemy = [], [], None, None, None
        player_y_vel = 0
        checkpoint_done = False
        message_text, message_time = "", 0

        for y, row in enumerate(level):
            for x, char in enumerate(row):
                if char == "#":
                    blocks.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == "P":
                    player = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 40, 40)
                elif char == "G":
                    goal = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                elif char == "E":
                    enemy = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE+10, 30, 30)
                    enemy_start_x, enemy_speed = enemy.x, 2
                elif char == "C":
                    checkpoints.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        exit_btn = pygame.Rect(950, 10, 40, 40)
        enemy_dir = 1

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

            dx = -5 if keys[pygame.K_LEFT] else 5 if keys[pygame.K_RIGHT] else 0
            player.x += dx
            for b in blocks:
                if player.colliderect(b):
                    player.right = b.left if dx>0 else player.left
                    player.left = b.right if dx<0 else player.right

            player_y_vel += 0.6
            player.y += int(player_y_vel)
            for b in blocks:
                if player.colliderect(b):
                    if player_y_vel > 0: player.bottom, player_y_vel = b.top, 0
                    if player_y_vel < 0: player.top, player_y_vel = b.bottom, 0

            # ---------- Enemy AI ----------
            if enemy:
                distance = player.x - enemy.x
                if abs(distance) < 200 and abs(player.y - enemy.y) < TILE_SIZE:
                    enemy.x += enemy_speed if distance > 0 else -enemy_speed
                # Ne essen le
                enemy_below = enemy.copy(); enemy_below.y += 1
                if not any(enemy_below.colliderect(b) for b in blocks):
                    enemy.x -= enemy_speed * enemy_dir
                if player.colliderect(enemy):
                    res = run_game_over(screen)
                    if res in ["restart", "menu", "exit"]: return res

            # ---------- Checkpoint és cél ----------
            if player.colliderect(goal):
                if not checkpoint_done:
                    message_text, message_time = "MENJ A CHECKPOINTHOZ!", pygame.time.get_ticks()+1500
                else:
                    screen.fill(BLACK)
                    draw_message(screen, "WIN", GREEN, y=HEIGHT//2-50)
                    pygame.display.flip(); time.sleep(2)
                    return "menu"

            if not checkpoint_done:
                for c in checkpoints:
                    if player.colliderect(c):
                        result = run_quiz(screen, level_number)
                        if result=="correct":
                            checkpoint_done=True
                            message_text, message_time="HELYES VÁLASZ!",pygame.time.get_ticks()+1200
                        else:
                            res = run_game_over(screen)
                            if res in ["restart","menu","exit"]: return res

            # ---------- Rajzolás ----------
            screen.fill(SKY)
            for b in blocks: pygame.draw.rect(screen, BLACK, b)
            for c in checkpoints: pygame.draw.rect(screen, YELLOW, c)
            pygame.draw.rect(screen, RED, player)
            pygame.draw.rect(screen, GREEN, goal)
            pygame.draw.rect(screen, RED, exit_btn)
            pygame.draw.line(screen, WHITE, (955,15),(985,45),4)
            pygame.draw.line(screen, WHITE, (985,15),(955,45),4)
            if enemy: pygame.draw.rect(screen, BLUE, enemy)
            if message_text and pygame.time.get_ticks()<message_time:
                draw_message(screen, message_text, GREEN if "HELYES" in message_text else RED)
            else: message_text=""
            pygame.display.flip(); clock.tick(FPS)
