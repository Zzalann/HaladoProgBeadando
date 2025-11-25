import pygame

WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (200, 0, 0)
HOVER = (90, 90, 90)
BLACK = (0, 0, 0)

def draw_button(screen, rect, text, base, hover, text_color):
    mx, my = pygame.mouse.get_pos()
    color = hover if rect.collidepoint(mx, my) else base
    pygame.draw.rect(screen, BLACK, rect.inflate(4, 4), border_radius=10)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))

def draw_title(screen, text):
    font = pygame.font.SysFont(None, 80)
    t = font.render(text, True, WHITE)
    screen.blit(t, (WIDTH//2 - t.get_width()//2, 50))

def run_menu(screen):
    clock = pygame.time.Clock()
    start = pygame.Rect(350, 220, 300, 70)
    exit_b = pygame.Rect(350, 320, 300, 70)

    while True:
        screen.fill((20,20,20))
        draw_title(screen, "Platformer Project")

        draw_button(screen, start, "Pályaválasztás", GRAY, HOVER, WHITE)
        draw_button(screen, exit_b, "Kilépés", RED, (255,50,50), WHITE)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(event.pos):
                    return "level_select"
                if exit_b.collidepoint(event.pos):
                    return "exit"

def run_level_select(screen, completed_levels):
    clock = pygame.time.Clock()

    lvl1 = pygame.Rect(350, 150, 300, 70)
    lvl2 = pygame.Rect(350, 240, 300, 70)
    lvl3 = pygame.Rect(350, 330, 300, 70)
    back = pygame.Rect(350, 430, 300, 70)

    warning_time = 0
    warning_text = ""

    while True:
        screen.fill((30,30,30))
        draw_title(screen, "Pályaválasztás")

        draw_button(screen, lvl1, "1. Pálya", GRAY, HOVER, WHITE)

        col2 = GRAY if completed_levels[1] else (80,80,80)
        col3 = GRAY if completed_levels[2] else (80,80,80)

        draw_button(screen, lvl2, "2. Pálya", col2, HOVER, WHITE)
        draw_button(screen, lvl3, "3. Pálya", col3, HOVER, WHITE)
        draw_button(screen, back, "Vissza", RED, (255,50,50), WHITE)

        if warning_text and pygame.time.get_ticks() < warning_time:
            font = pygame.font.SysFont(None, 40)
            t = font.render(warning_text, True, (255,50,50))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 520))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if lvl1.collidepoint((mx, my)):
                    return 1

                if lvl2.collidepoint((mx, my)):
                    if completed_levels[1]:
                        return 2
                    else:
                        warning_text = "Előbb teljesítsd az 1. pályát!"
                        warning_time = pygame.time.get_ticks() + 2000

                if lvl3.collidepoint((mx, my)):
                    if completed_levels[2]:
                        return 3
                    else:
                        warning_text = "Előbb teljesítsd a megelőző pályákat!"
                        warning_time = pygame.time.get_ticks() + 2000

                if back.collidepoint((mx, my)):
                    return "back"

def run_game_over(screen):
    global WIDTH, HEIGHT, BLACK, RED, GRAY, HOVER, WHITE  # Használja a globális színeket

    clock = pygame.time.Clock()

    retry_b = pygame.Rect(350, 300, 300, 70)  # Újrapróbálás
    menu_b = pygame.Rect(350, 390, 300, 70)  # Főmenü

    while True:
        screen.fill(BLACK)

        font_title = pygame.font.SysFont(None, 120, bold=True)
        t_title = font_title.render("GAME OVER", True, RED)
        screen.blit(t_title, (WIDTH // 2 - t_title.get_width() // 2, 100))

        font_msg = pygame.font.SysFont(None, 40)
        t_msg = font_msg.render("Az ellenség elkapott!", True, WHITE)
        screen.blit(t_msg, (WIDTH // 2 - t_msg.get_width() // 2, 210))

        draw_button(screen, retry_b, "Újrapróbálás", GRAY, HOVER, WHITE)
        draw_button(screen, menu_b, "Főmenü", RED, (255, 50, 50), WHITE)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if retry_b.collidepoint((mx, my)):
                    return "retry"

                if menu_b.collidepoint((mx, my)):
                    return "menu"

