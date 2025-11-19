import pygame

WIDTH, HEIGHT = 1000, 600

def draw_button(screen, text, x, y, w, h):

    rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(screen, (50, 50, 50), rect)

    font = pygame.font.SysFont(None, 50)

    t = font.render(text, True, (255, 255, 255))

    screen.blit(t, (x + 20, y + 15))

    return rect

def run_menu(screen):

    clock = pygame.time.Clock()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos

                if b1.collidepoint(mx, my):

                    return "level_select"

                if b2.collidepoint(mx, my):

                    return "exit"

        screen.fill((20, 20, 20))

        b1 = draw_button(screen, "Palyavalasztas", 350, 200, 300, 70)

        b2 = draw_button(screen, "Kilepes", 350, 300, 300, 70)

        pygame.display.flip()

        clock.tick(60)

def run_level_select(screen):

    clock = pygame.time.Clock()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return "back"

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos

                if b1.collidepoint(mx,my):

                    return 1

                if b2.collidepoint(mx,my):

                    return 2

                if b3.collidepoint(mx,my):

                    return 3

                if b4.collidepoint(mx,my):

                    return "back"

        screen.fill((30, 30, 30))

        b1 = draw_button(screen, "1. Palya", 350, 150, 300, 70)

        b2 = draw_button(screen, "2. Palya", 350, 240, 300, 70)

        b3 = draw_button(screen, "3. Palya", 350, 330, 300, 70)

        b4 = draw_button(screen, "Vissza",   350, 420, 300, 70)

        pygame.display.flip()

        clock.tick(60)
 