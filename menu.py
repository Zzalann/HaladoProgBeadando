import pygame

WIDTH, HEIGHT = 1000, 600

# ---------- Színek ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BUTTON_HOVER = (70, 70, 70)
RED = (200, 0, 0)
DARK_GRAY = (30, 30, 30)

# ---------- Segédfüggvény ----------
def draw_button(screen, rect, text, base_color, hover_color, text_color):
    mx, my = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mx, my) else base_color
    pygame.draw.rect(screen, BLACK, rect.inflate(4,4), border_radius=10)  # keret
    pygame.draw.rect(screen, color, rect, border_radius=10)
    font = pygame.font.SysFont(None, 40)
    t = font.render(text, True, text_color)
    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))

def draw_title(screen, text):
    font = pygame.font.SysFont(None, 70)
    t = font.render(text, True, WHITE)
    screen.blit(t, (WIDTH//2 - t.get_width()//2, 50))

# ---------- Főmenü ----------
def run_menu(screen):
    clock = pygame.time.Clock()
    b1 = pygame.Rect(350, 200, 300, 70)
    b2 = pygame.Rect(350, 300, 300, 70)

    while True:
        screen.fill((20, 20, 20))
        draw_title(screen, "Platformer Project")

        draw_button(screen, b1, "Pályaválasztás", GRAY, BUTTON_HOVER, WHITE)
        draw_button(screen, b2, "Kilépés", RED, (255,50,50), WHITE)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if b1.collidepoint(mx, my):
                    return "level_select"
                if b2.collidepoint(mx, my):
                    return "exit"

# ---------- Pályaválasztó ----------
def run_level_select(screen):
    clock = pygame.time.Clock()
    b1 = pygame.Rect(350, 150, 300, 70)
    b2 = pygame.Rect(350, 240, 300, 70)
    b3 = pygame.Rect(350, 330, 300, 70)
    b4 = pygame.Rect(350, 420, 300, 70)

    while True:
        screen.fill(DARK_GRAY)
        draw_title(screen, "Pályaválasztás")

        draw_button(screen, b1, "1. Pálya", GRAY, BUTTON_HOVER, WHITE)
        draw_button(screen, b2, "2. Pálya", GRAY, BUTTON_HOVER, WHITE)
        draw_button(screen, b3, "3. Pálya", GRAY, BUTTON_HOVER, WHITE)
        draw_button(screen, b4, "Vissza", RED, (255,50,50), WHITE)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if b1.collidepoint(mx, my): return 1
                if b2.collidepoint(mx, my): return 2
                if b3.collidepoint(mx, my): return 3
                if b4.collidepoint(mx, my): return "back"