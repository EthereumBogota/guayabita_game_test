import os
import pygame
import pygame_gui
import sys
import random
import math
import numpy as np

# Inicializar Pygame
pygame.init()

ORIGIN_FONT = os.environ["ORIGIN_FONT"]

POLYGON = (123, 63, 228)  # Color de la mitad izquierda
AVALANCHE = (232, 65, 66)  # Color de la mitad derecha
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (82, 80, 89)

WIDTH, HEIGHT = 900, 900

title_font = pygame.font.Font(ORIGIN_FONT, 50)
small_font = pygame.font.Font(ORIGIN_FONT, 25)
input_font = pygame.font.Font(ORIGIN_FONT, 18)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

pygame.display.set_caption("GuayabitaWeb3Game")

clock = pygame.time.Clock()
html_text = 0

polygon_radius = int(WIDTH // 5)
dice_size = int(WIDTH // 5)

num_sides = 16

dice_value = random.randint(1, 6)

pygame.draw.rect(screen, POLYGON, (0, 0, WIDTH // 2, HEIGHT))
pygame.draw.rect(screen, AVALANCHE, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

imagen = pygame.image.load('img/logo.png')
imagen = pygame.transform.scale(imagen, (200, 200))

text_box_1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, HEIGHT - 70), (200, 50)),
                                                 manager=manager)

button_rect = pygame.Rect((WIDTH // 2 - 50, HEIGHT - 70), (90, 50))
button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                      text='play!',
                                      manager=manager)


def draw_text(text, x, y, color=WHITE):
    text_surface = title_font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_text_small(text, x, y, color=WHITE):
    text_surface = small_font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Función para dibujar el dado
def draw_square(surface, value, x, y):
    pygame.draw.rect(surface, GRAY, (x, y, dice_size, dice_size))  # Dado
    text = title_font.render("", True, WHITE)
    surface.blit(text, (x + dice_size // 4, y + dice_size // 4))


# Función para dibujar un polígono regular
def draw_polygon(surface, color, n_sides, radius, center, border=0):
    points = []
    for i in range(n_sides):
        angle = 2 * math.pi * i / n_sides
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width=border)


def draw_dice_anim(side: int, radius: int = 20, border_height: int = 50):
    if side in {1, 3, 5}:
        pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), radius)
    if side in {2, 3, 4, 5, 6}:
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 - border_height, HEIGHT // 2 - border_height), radius)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 + border_height, HEIGHT // 2 + border_height), radius)
    if side in {4, 5, 6}:
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 - border_height, HEIGHT // 2 + border_height), radius)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 + border_height, HEIGHT // 2 - border_height), radius)
    if side == 6:
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 - border_height, HEIGHT // 2), radius)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 + border_height, HEIGHT // 2), radius)
    pygame.display.flip()


# Bucle principal del juego
while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Cambiar el side del dado manteniendo el anterior
                dice_value = random.randint(1, 6)
                html_text = random.randint(10, 40)

        manager.process_events(event)

    ui_events = pygame.event.get(pygame.USEREVENT)
    for event in ui_events:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                # Cambiar el side del dado al hacer clic en el botón
                dice_value = random.randint(1, 6)
                html_text = random.randint(10, 40)

    text_box_2 = pygame_gui.elements.UITextBox(str(html_text),
                                               relative_rect=pygame.Rect((WIDTH - 410, HEIGHT - 70),
                                                                         (200, 50)))

    manager.update(time_delta)

    draw_polygon(screen, WHITE, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 0)
    draw_polygon(screen, GRAY, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 14)

    draw_square(screen, dice_value, WIDTH // 2 - dice_size // 2, HEIGHT // 2 - dice_size // 2)

    draw_dice_anim(side=dice_value)

    draw_text('Polygon', 80, 10, AVALANCHE)
    draw_text('Avalanch', WIDTH - title_font.size('Avalanch')[0] - 70, 10, POLYGON)
    draw_text('Pool: ', WIDTH // 2 - title_font.size('Pool')[0], 100, GRAY)

    draw_text_small('hash: ', 80, 60, WHITE)

    screen.blit(imagen, ((WIDTH - imagen.get_width()) + 10, (HEIGHT - imagen.get_height()) - 10))

    manager.draw_ui(screen)

    pygame.display.update()
