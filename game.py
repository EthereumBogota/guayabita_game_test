import os
import sys
import VRF
import math
import pygame
import random
import warnings
import pygame_gui
from pygame.math import Vector2
warnings.filterwarnings("ignore", category=DeprecationWarning)

pygame.init()

ORIGIN_FONT = os.environ["ORIGIN_FONT"]

POLYGON = (123, 63, 228)  # Color de la mitad izquierda
AVALANCHE = (232, 65, 66)  # Color de la mitad derecha
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (82, 80, 89)
BLUE = (76, 109, 243)
GREEN = (35, 177, 77)

WIDTH, HEIGHT = 900, 900

title_font = pygame.font.Font(ORIGIN_FONT, 50)
small_font = pygame.font.Font(ORIGIN_FONT, 25)
input_font = pygame.font.Font(ORIGIN_FONT, 10)

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

show_lose_text = False
lose_text_position = Vector2(title_font.size(f'house wins! {str(text_box_1.text)}')[0] + 10, 60)

show_win_text = False
win_text_position = Vector2(WIDTH - title_font.size('you win!')[0] + 20, 60)


def draw_text(text, x, y, color=WHITE):
    """
    this funtion draw simple text
    :param text: str, text to render
    :param x: int, x position
    :param y: int, y position
    :param color: tuple, color
    :return:
    """
    text_surface = title_font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_text_small(text, x, y, color=WHITE):
    """
    this funtion draw small text
    :param text: str, text to render
    :param x: int, x position
    :param y: int, y position
    :param color: tuple, color
    :return:
    """
    text_surface = small_font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_square(surface, value, x, y):
    """
    this function draw dice
    :param surface:
    :param value:
    :param x:
    :param y:
    :return:
    """
    pygame.draw.rect(surface, GRAY, (x, y, dice_size, dice_size))  # Dado
    text = title_font.render("", True, WHITE)
    surface.blit(text, (x + dice_size // 4, y + dice_size // 4))


def draw_polygon(surface, color, n_sides, radius, center, border=0):
    """
    this funtion create a polygon round dice
    :param surface:
    :param color:
    :param n_sides: int, polygon sides
    :param radius: int, radius polygon
    :param center: int, center polygon
    :param border: int, fill polygon
    :return:
    """
    points = []
    for i in range(n_sides):
        angle = 2 * math.pi * i / n_sides
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width=border)


def draw_dice_anim(side: int, radius: int = 20, border_height: int = 50):
    """
    this funtion crea dice animation
    :param side: int, side
    :param radius: int, radius dice
    :param border_height: int
    :return:
    """
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


# create random seed with
random_seed = VRF.oracle_random_number()
random.seed(random_seed)

# Bucle principal del juego
while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dice_value = random.randint(1, 6)
                html_text = random.randint(10, 28)
                show_lose_text = (dice_value == 1)
                show_win_text = (dice_value == 6)

        manager.process_events(event)

    ui_events = pygame.event.get(pygame.USEREVENT)
    for event in ui_events:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                dice_value = random.randint(1, 6)
                html_text = random.randint(10, 28)
                show_lose_text = (dice_value == 1)
                show_win_text = (dice_value == 6)

    text_box_2 = pygame_gui.elements.UITextBox(str(html_text),
                                               relative_rect=pygame.Rect((WIDTH - 410, HEIGHT - 70),
                                                                         (200, 50)))

    manager.update(time_delta)

    if show_win_text:
        win_text_position.x -= 50 * time_delta  # Velocidad del desplazamiento
        pygame.draw.rect(screen, POLYGON, (0, 0, WIDTH // 2, HEIGHT))
        pygame.draw.rect(screen, AVALANCHE, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))
        screen.blit(imagen, ((WIDTH - imagen.get_width()) + 10, (HEIGHT - imagen.get_height()) - 10))

    if show_lose_text:
        lose_text_position.x += 50 * time_delta  # Velocidad del desplazamiento
        pygame.draw.rect(screen, POLYGON, (0, 0, WIDTH // 2, HEIGHT))
        pygame.draw.rect(screen, AVALANCHE, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))
        screen.blit(imagen, ((WIDTH - imagen.get_width()) + 10, (HEIGHT - imagen.get_height()) - 10))

    draw_polygon(screen, WHITE, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 0)
    draw_polygon(screen, GRAY, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 14)

    draw_square(screen, dice_value, WIDTH // 2 - dice_size // 2, HEIGHT // 2 - dice_size // 2)

    draw_dice_anim(side=dice_value)

    draw_text('Polygon', 80, 10, AVALANCHE)
    draw_text('Avalanche', WIDTH - title_font.size('Avalanch')[0] - 100, 10, POLYGON)
    # draw_text('Pool: ', WIDTH // 2 - title_font.size('Pool')[0], 100, GRAY)

    # draw_text_small(f'random seed {random_seed}', 80, 700, WHITE)

    screen.blit(imagen, ((WIDTH - imagen.get_width()) + 10, (HEIGHT - imagen.get_height()) - 10))

    if show_win_text:
        win_text_position.x -= 50 * time_delta  # Reducir la velocidad de desplazamiento
        draw_text(f'You win! {html_text}', int(win_text_position.x), int(win_text_position.y), GREEN)

        if win_text_position.x < title_font.size('You win!')[0]:
            html_text = 0
            win_text_position = Vector2(WIDTH - title_font.size('you win!')[0] + 20, 60)
            show_win_text = False
            pygame.draw.rect(screen, POLYGON, (0, 0, WIDTH // 2, HEIGHT))
            pygame.draw.rect(screen, AVALANCHE, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

    if show_lose_text:
        lose_text_position.x += 50 * time_delta  # Reducir la velocidad de desplazamiento
        draw_text(f'house wins! {str(text_box_1.text)}', int(lose_text_position.x), int(lose_text_position.y), BLUE)

        if lose_text_position.x > WIDTH - title_font.size(f'house wins! {str(text_box_1.text)}')[0]:
            text_box_1.set_text('0')
            lose_text_position = Vector2(title_font.size(f'house wins! {str(text_box_1.text)}')[0] + 10, 60)
            show_lose_text = False
            pygame.draw.rect(screen, POLYGON, (0, 0, WIDTH // 2, HEIGHT))
            pygame.draw.rect(screen, AVALANCHE, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

    manager.draw_ui(screen)

    pygame.display.update()
