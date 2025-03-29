# Nicolas Expedito Lana Mendes 22.1.4028
import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atividade 5: Fundamentos de Programação Gráfica")
clock = pygame.time.Clock()


# 1 - Exercício 1
# 2 - Exercício 2
mode = 1

# Função para desenhar um triângulo com gradiente de cores
def draw_gradient_triangle(surface, vertices, colors):
    (x0, y0), (x1, y1), (x2, y2) = vertices
    # Determina o retângulo delimitador do triângulo
    min_x = int(min(x0, x1, x2))
    max_x = int(max(x0, x1, x2))
    min_y = int(min(y0, y1, y2))
    max_y = int(max(y0, y1, y2))
    # Calcula o denominador para as coordenadas baricêntricas
    denom = ((y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2))
    if denom == 0:
        return  # Triângulo degenerado
    # Varre os pixels dentro da caixa delimitadora
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # Calcula as coordenadas baricêntricas
            alpha = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / denom
            beta = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / denom
            gamma = 1 - alpha - beta
            # Se o ponto (x,y) estiver dentro do triângulo
            if alpha >= 0 and beta >= 0 and gamma >= 0:
                r = int(alpha * colors[0][0] + beta * colors[1][0] + gamma * colors[2][0])
                g = int(alpha * colors[0][1] + beta * colors[1][1] + gamma * colors[2][1])
                b = int(alpha * colors[0][2] + beta * colors[1][2] + gamma * colors[2][2])
                surface.set_at((x, y), (r, g, b))

# Variáveis para o Exercício 2: Quadrado móvel
square_size = 50
square_x = WIDTH // 2 - square_size // 2
square_y = HEIGHT // 2 - square_size // 2
square_speed = 5

# Fonte para exibir textos
font = pygame.font.SysFont(None, 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2

    keys = pygame.key.get_pressed()
    if mode == 2:
        # Processa o movimento do quadrado com as setas do teclado
        if keys[pygame.K_LEFT]:
            square_x -= square_speed
        if keys[pygame.K_RIGHT]:
            square_x += square_speed
        if keys[pygame.K_UP]:
            square_y -= square_speed
        if keys[pygame.K_DOWN]:
            square_y += square_speed
        # Limita o quadrado para que ele não saia da tela
        square_x = max(0, min(WIDTH - square_size, square_x))
        square_y = max(0, min(HEIGHT - square_size, square_y))
    
    screen.fill((0, 0, 0))
    if mode == 1:
        # Exercício 1: Desenha o triângulo com gradiente
        vertices = [(200, 100), (100, 300), (300, 300)]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # vermelho, verde e azul
        draw_gradient_triangle(screen, vertices, colors)
        text = font.render("Exercício 1: Triângulo com gradiente", True, (255, 255, 255))
        screen.blit(text, (20, 20))
    elif mode == 2:
        # Exercício 2: Desenha o quadrado móvel
        pygame.draw.rect(screen, (0, 255, 255), (square_x, square_y, square_size, square_size))
        text = font.render("Exercício 2: Quadrado móvel (use as setas)", True, (255, 255, 255))
        screen.blit(text, (20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
