import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tamaño de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación de Texto")

# Configurar el reloj
clock = pygame.time.Clock()

# Fuente y tamaño del texto
font = pygame.font.Font(None, 36)

# Texto inicial
text_surface = font.render("¡Animación de Texto!", True, WHITE)
text_rect = text_surface.get_rect()
text_rect.center = (WIDTH // 2, HEIGHT // 2)

# Velocidad de desplazamiento
speed = 5

# Inicializar la variable de animación
animation_started = False

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Iniciar animación al presionar la barra espaciadora
        initial_position = text_rect.x
        target_position = WIDTH  # Puedes ajustar esto según sea necesario
        animation_started = True

    if animation_started:
        # Mover el texto hacia la derecha
        text_rect.x += speed
        if text_rect.x > target_position:
            text_rect.x = initial_position  # Reiniciar la animación al llegar al final
            animation_started = False

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar el texto en su nueva posición
    screen.blit(text_surface, text_rect)

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer la velocidad del juego
    clock.tick(60)  # Ajusta la velocidad de la animación según sea necesario

# Salir del juego
pygame.quit()
sys.exit()
