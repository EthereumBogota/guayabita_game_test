import pygame
import sys
import random
import math
import numpy as np

# Inicializar Pygame
pygame.init()

POLYGON = (123, 63, 228)  # Color de la mitad izquierda
AVALANCHE = (232, 65, 66)  # Color de la mitad derecha
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (82, 80, 89)

# Tamaño de la pantalla
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GuayabitaWeb3Game")

# Configurar el reloj
clock = pygame.time.Clock()

# Tamaño del polígono y dado
polygon_radius = int(WIDTH // 5)
dice_size = int(WIDTH // 5)

# Número de lados del polígono
num_sides = 16

# side del dado
dice_value = random.randint(1, 6)


# Función para dibujar el dado
def draw_dice(surface, value, x, y):
    pygame.draw.rect(surface, GRAY, (x, y, dice_size, dice_size))  # Dado
    font = pygame.font.Font(None, 36)
    text = font.render(str(value), True, WHITE)
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Cambiar el side del dado manteniendo el anterior
                dice_value = random.randint(1, 6)

    # Dibujar la pantalla dividida
    pygame.draw.rect(screen, POLYGON, (0, 0, WIDTH // 2, HEIGHT))
    pygame.draw.rect(screen, AVALANCHE, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

    # Dibujar el polígono WHITE en el centro (20% más grande)
    draw_polygon(screen, WHITE, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 0)
    draw_polygon(screen, GRAY, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 8)

    # Dibujar el dado en el polígono
    draw_dice(screen, dice_value, WIDTH // 2 - dice_size // 2, HEIGHT // 2 - dice_size // 2)

    draw_dice_anim(side=dice_value)

    # Establecer la velocidad del juego
    clock.tick(5)  # Cambia este side según lo rápido que quieras que cambie el dado
