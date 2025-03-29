# Nicolas Expedito Lana Mendes 22.1.4028
import pygame
import math

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Transformações Geométricas - Atividade 3")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Funções de transformação
def rotate_2d(points, angle, center):
    rotated_points = []
    angle_rad = math.radians(angle)
    for x, y in points:
        x -= center[0]
        y -= center[1]
        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        new_x += center[0]
        new_y += center[1]
        rotated_points.append((new_x, new_y))
    return rotated_points

def scale_3d(points_3d, scale_factor):
    return [(x * scale_factor, y * scale_factor, z * scale_factor) 
            for x, y, z in points_3d]

def project_3d_to_2d(points_3d, distance=200):
    projected = []
    for x, y, z in points_3d:
        factor = distance / (distance + z)
        x_2d = x * factor + WIDTH/2
        y_2d = y * factor + HEIGHT/2
        projected.append((x_2d, y_2d))
    return projected

def compose_2d(points, angle, scale, center):
    rotated = rotate_2d(points, angle, center)
    scaled = []
    for x, y in rotated:
        x = (x - center[0]) * scale + center[0]
        y = (y - center[1]) * scale + center[1]
        scaled.append((x, y))
    return scaled

def compose_3d(points_3d, angle_y, translation):
    composed = []
    angle_rad = math.radians(angle_y)
    for x, y, z in points_3d:
        new_x = z * math.sin(angle_rad) + x * math.cos(angle_rad)
        new_z = z * math.cos(angle_rad) - x * math.sin(angle_rad)
        new_y = y
        new_x += translation[0]
        new_y += translation[1]
        new_z += translation[2]
        composed.append((new_x, new_y, new_z))
    return composed

# Objetos iniciais
rect_2d = [(200, 200), (300, 200), (300, 300), (200, 300)]
cube_3d = [(-50, -50, -50), (50, -50, -50), (50, 50, -50), (-50, 50, -50),
          (-50, -50, 50), (50, -50, 50), (50, 50, 50), (-50, 50, 50)]

# Variáveis de controle
angle = 0
current_scene = 1  # Começa na cena a)
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_scene = 1  # a) 
            elif event.key == pygame.K_2:
                current_scene = 2  # b) 
            elif event.key == pygame.K_3:
                current_scene = 3  # c)
            elif event.key == pygame.K_4:
                current_scene = 4  # d)

    screen.fill(BLACK)

    #  Rotação 2D
    if current_scene == 1:
        center_2d = (250, 250)
        rotated_rect = rotate_2d(rect_2d, angle, center_2d)
        pygame.draw.polygon(screen, RED, rotated_rect, 2)
        text = font.render("a) Rotação 2D (Tecla 1)", True, WHITE)
        screen.blit(text, (10, 10))

    #  Escala 3D
    elif current_scene == 2:
        scaled_cube = scale_3d(cube_3d, 1 + math.sin(angle/20)/2)
        projected_scaled = project_3d_to_2d(scaled_cube)
        for i in range(4):
            pygame.draw.line(screen, BLUE, projected_scaled[i], projected_scaled[(i+1)%4], 1)
            pygame.draw.line(screen, BLUE, projected_scaled[i+4], projected_scaled[(i+1)%4+4], 1)
            pygame.draw.line(screen, BLUE, projected_scaled[i], projected_scaled[i+4], 1)
        text = font.render("b) Escala 3D (Tecla 2)", True, WHITE)
        screen.blit(text, (10, 10))

    #  Composição 2D
    elif current_scene == 3:
        center_2d = (250, 250)
        composed_2d = compose_2d(rect_2d, angle, 1.5, center_2d)
        pygame.draw.polygon(screen, GREEN, composed_2d, 2)
        text = font.render("c) Rotação + Escala 2D (Tecla 3)", True, WHITE)
        screen.blit(text, (10, 10))

    # Composição 3D
    elif current_scene == 4:
        composed_3d = compose_3d(cube_3d, angle, (0, 0, 50))
        projected_composed = project_3d_to_2d(composed_3d)
        for i in range(4):
            pygame.draw.line(screen, WHITE, projected_composed[i], projected_composed[(i+1)%4], 1)
            pygame.draw.line(screen, WHITE, projected_composed[i+4], projected_composed[(i+1)%4+4], 1)
            pygame.draw.line(screen, WHITE, projected_composed[i], projected_composed[i+4], 1)
        text = font.render("d) Rotação Y + Translação 3D (Tecla 4)", True, WHITE)
        screen.blit(text, (10, 10))

    # Instruções
    instructions = font.render("Use teclas 1-4 para mudar entre transformações", True, WHITE)
    screen.blit(instructions, (10, HEIGHT - 40))

    angle += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()