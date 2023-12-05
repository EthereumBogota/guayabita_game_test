import pygame
import sys
import random
import math

# Inicializar Pygame
pygame.init()

# Definir colores retro
COLOR1 = (30, 30, 30)  # Color de la mitad izquierda
COLOR2 = (100, 100, 100)  # Color de la mitad derecha
WHITE = (255, 255, 255)  # Color blanco para el polígono
RED = (255, 0, 0)  # Color del dado (puedes ajustarlo según tu paleta)

# Tamaño de la pantalla
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GuayabitaWeb3Game")

# Configurar el reloj
clock = pygame.time.Clock()

# Tamaño del polígono y dado
polygon_radius = int(WIDTH // 5)
dice_size = int(WIDTH // 5)

# Número de lados del polígono
num_sides = 16

# Valor del dado
dice_value = 1


# Función para dibujar el dado
def draw_dice(surface, value, x, y):
    pygame.draw.rect(surface, RED, (x, y, dice_size, dice_size))  # Dado
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


# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Cambiar el valor del dado manteniendo el anterior
                dice_value = random.randint(1, 6)

    # Dibujar la pantalla dividida
    pygame.draw.rect(screen, COLOR1, (0, 0, WIDTH // 2, HEIGHT))
    pygame.draw.rect(screen, COLOR2, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

    # Dibujar el polígono blanco en el centro (20% más grande)
    draw_polygon(screen, WHITE, num_sides, polygon_radius,(WIDTH // 2, HEIGHT // 2), 0)
    draw_polygon(screen, RED, num_sides, polygon_radius, (WIDTH // 2, HEIGHT // 2), 8)

    # Dibujar el dado en el polígono
    draw_dice(screen, dice_value, WIDTH // 2 - dice_size // 2, HEIGHT // 2 - dice_size // 2)

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer la velocidad del juego
    clock.tick(5)  # Cambia este valor según lo rápido que quieras que cambie el dado
