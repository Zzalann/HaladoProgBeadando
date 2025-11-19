import pygame
import time
import random

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
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.x + 10, rect.y + 10))

def run_quiz(screen, level_number):
    if level_number == 1:
        questions = [
            ["Milyen szinű a fű?", ["Kék", "Zöld", "Piros", "Fehér"], 1],
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
                    mx, my = event.pos
                    if exit_btn.collidepoint(mx, my):
                        return "menu"

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

            if player.colliderect(goal):
                if not checkpoint_done:
                    message_text = "MENJ A CHECKPOINTHOZ!"
                    message_time = pygame.time.get_ticks() + 1500
                else:
                    screen.fill((0, 0, 0))
                    font = pygame.font.SysFont(None, 100)
                    win = font.render("WIN", True, (0, 255, 0))
                    screen.blit(win, (WIDTH//2 - 100, HEIGHT//2 - 50))
                    pygame.display.flip()
                    time.sleep(2)
                    return "menu"

            if not checkpoint_done:
                for c in checkpoints:
                    if player.colliderect(c):
                        result = run_quiz(screen, level_number)

                        if result == "correct":
                            checkpoint_done = True
                            message_text = "HELYES VÁLASZ!"
                            message_time = pygame.time.get_ticks() + 1200

                        elif result == "wrong":
                            for _ in range(30):
                                screen.fill((135, 206, 235))
                                for b in blocks:
                                    pygame.draw.rect(screen, (0, 0, 0), b)
                                for cc in checkpoints:
                                    pygame.draw.rect(screen, (255, 255, 0), cc)
                                pygame.draw.rect(screen, (255, 0, 0), player)
                                pygame.draw.rect(screen, (0, 255, 0), goal)

                                font = pygame.font.SysFont(None, 40)
                                msg = font.render("ROSSZ VÁLASZ!", True, (255, 0, 0))
                                pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2 - 200, 20, 400, 40))
                                screen.blit(msg, (WIDTH//2 - 180, 25))

                                pygame.display.flip()
                                clock.tick(60)

                            return "restart"

                        else:
                            return "menu"

            screen.fill((135, 206, 235))

            for b in blocks:
                pygame.draw.rect(screen, (0, 0, 0), b)

            for c in checkpoints:
                pygame.draw.rect(screen, (255, 255, 0), c)

            pygame.draw.rect(screen, (255, 0, 0), player)
            pygame.draw.rect(screen, (0, 255, 0), goal)

            pygame.draw.rect(screen, (255, 0, 0), exit_btn)
            pygame.draw.line(screen, (255, 255, 255), (955, 15), (985, 45), 4)
            pygame.draw.line(screen, (255, 255, 255), (985, 15), (955, 45), 4)

            if enemy:
                pygame.draw.rect(screen, (0, 0, 255), enemy)

            if message_text and pygame.time.get_ticks() < message_time:
                font = pygame.font.SysFont(None, 40)
                color = (0, 200, 0) if "HELYES" in message_text else (255, 0, 0)
                msg = font.render(message_text, True, color)
                pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2 - 200, 20, 400, 40))
                screen.blit(msg, (WIDTH//2 - 180, 25))

            else:
                message_text = ""

            pygame.display.flip()
            clock.tick(60)
