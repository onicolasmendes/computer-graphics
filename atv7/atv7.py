# Nicolas Expedito Lana Mendes 22.1.4028
import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atividade 7: Labirinto 3D e Cubo Animado - Pygame")
clock = pygame.time.Clock()

# Seleção de modo: 1 = Labirinto , 2 = Cubo
mode = 1

# Exercício 7.1: Labirinto 3D 
# Mapa do labirinto: 1 = parede, 0 = espaço livre
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]
TILE_SIZE = 64
MAP_WIDTH = len(maze[0])
MAP_HEIGHT = len(maze)

# Posição e ângulo do jogador
player_x = TILE_SIZE * 1.5
player_y = TILE_SIZE * 1.5
player_angle = 0

# Parâmetros do raycasting
FOV = math.pi / 3  # 60°
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
SCALE = WIDTH // NUM_RAYS
STEP = 4  

def cast_rays():
    # Desenha piso e teto
    pygame.draw.rect(screen, (100,100,100), (0, HEIGHT//2, WIDTH, HEIGHT//2))   
    pygame.draw.rect(screen, (70,70,70), (0, 0, WIDTH, HEIGHT//2))               

    cur_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(1, MAX_DEPTH):
            target_x = player_x + depth * cos_a
            target_y = player_y + depth * sin_a
            i = int(target_x / TILE_SIZE)
            j = int(target_y / TILE_SIZE)
            if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT:
                if maze[j][i] == 1:
                    depth *= math.cos(player_angle - cur_angle)
                    # Calcula a altura da parede com base na distância
                    wall_height = 80000 / (depth + 0.0001)
                    shade = 255 / (1 + depth * depth * 0.0001)
                    color = (shade, shade, shade)
                    pygame.draw.rect(screen, color, (ray * SCALE, HEIGHT//2 - wall_height//2, SCALE, wall_height))
                    break
        cur_angle += DELTA_ANGLE

def move_player():
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    # Movimento: W e S para avançar/recuar
    if keys[pygame.K_w]:
        dx += STEP * math.cos(player_angle)
        dy += STEP * math.sin(player_angle)
    if keys[pygame.K_s]:
        dx -= STEP * math.cos(player_angle)
        dy -= STEP * math.sin(player_angle)
    # Strafing: A para esquerda, D para direita
    if keys[pygame.K_d]:
        dx += STEP * math.cos(player_angle + math.pi/2)
        dy += STEP * math.sin(player_angle + math.pi/2)
    if keys[pygame.K_a]:
        dx += STEP * math.cos(player_angle - math.pi/2)
        dy += STEP * math.sin(player_angle - math.pi/2)
    # Rotação: setas esquerda/direita para girar
    if keys[pygame.K_LEFT]:
        player_angle -= 0.03
    if keys[pygame.K_RIGHT]:
        player_angle += 0.03

    new_x = player_x + dx
    new_y = player_y + dy
    # Verificação de colisão
    i = int(new_x / TILE_SIZE)
    j = int(new_y / TILE_SIZE)
    if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT:
        if maze[j][i] == 0:
            player_x = new_x
            player_y = new_y

# Exercício 7.2: Cubo Animado com Projeção Alternada
# Parâmetros do cubo
cube_vertices = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)
]
cube_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

cube_angle = 0.0
cube_scale = 1.0
growing = True
projection_mode = "perspective" 

def rotate_y(point, theta):
    x, y, z = point
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return (x * cos_t + z * sin_t, y, -x * sin_t + z * cos_t)

def project_point(point):
    x, y, z = point
    if projection_mode == "perspective":
        d = 3
        factor = d / (z + d + 0.001)
        x, y = x * factor, y * factor
    return int(WIDTH/2 + x * 200), int(HEIGHT/2 - y * 200)

def get_transformed_cube():
    transformed = []
    for vertex in cube_vertices:
        # Aplica escala
        v = (vertex[0]*cube_scale, vertex[1]*cube_scale, vertex[2]*cube_scale)
        # Aplica rotação no eixo Y
        v = rotate_y(v, cube_angle)
        transformed.append(project_point(v))
    return transformed

def update_cube():
    global cube_angle, cube_scale, growing
    cube_angle += 0.01
    if growing:
        cube_scale += 0.005
        if cube_scale >= 2.0:
            growing = False
    else:
        cube_scale -= 0.005
        if cube_scale <= 0.5:
            growing = True

def draw_cube():
    points = get_transformed_cube()
    for edge in cube_edges:
        pygame.draw.line(screen, (255,255,255), points[edge[0]], points[edge[1]], 2)

# Loop Principal
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Alterna os modos de execução
            if event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
            # No modo cubo, alterna entre projeções
            if mode == 2:
                if event.key == pygame.K_p:
                    projection_mode = "perspective"
                elif event.key == pygame.K_o:
                    projection_mode = "orthogonal"

    if mode == 1:
        move_player()
        cast_rays()
    elif mode == 2:
        update_cube()
        draw_cube()
        font = pygame.font.SysFont(None, 24)
        text = font.render("Exercício 7.2: Pressione 'p' para perspectiva, 'o' para ortogonal", True, (255,255,255))
        screen.blit(text, (20,20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()