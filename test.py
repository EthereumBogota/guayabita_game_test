import pygame
import random

# Inicializar Pygame
pygame.init()

# Configurar la ventana
ancho, alto = 800, 600
ventana = pygame.display.set_mode((ancho, alto))

# Configurar los colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Configurar el dado
valor_dado = 1

# Función para dibujar el dado
def dibujar_dado(valor):
    ventana.fill(NEGRO)
    if valor in {1, 3, 5}:
        pygame.draw.circle(ventana, BLANCO, (ancho // 2, alto // 2), 10)
    if valor in {2, 3, 4, 5, 6}:
        pygame.draw.circle(ventana, BLANCO, (ancho // 2 - 100, alto // 2 - 100), 10)
        pygame.draw.circle(ventana, BLANCO, (ancho // 2 + 100, alto // 2 + 100), 10)
    if valor in {4, 5, 6}:
        pygame.draw.circle(ventana, BLANCO, (ancho // 2 - 100, alto // 2 + 100), 10)
        pygame.draw.circle(ventana, BLANCO, (ancho // 2 + 100, alto // 2 - 100), 10)
    if valor == 6:
        pygame.draw.circle(ventana, BLANCO, (ancho // 2 - 100, alto // 2), 10)
        pygame.draw.circle(ventana, BLANCO, (ancho // 2 + 100, alto // 2), 10)
    pygame.display.flip()

# Bucle principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                valor_dado = random.randint(1, 6)
    dibujar_dado(valor_dado)

pygame.quit()
