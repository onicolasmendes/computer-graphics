# Nicolas Expedito Lana Mendes 22.1.4028

import pygame
import math
import sys

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Exercícios 9.1 e 9.2 - Mapeamento de Textura e Recorte de Linhas")
clock = pygame.time.Clock()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Variável para controlar qual exercício está sendo exibido
current_exercise = 1  

## Exercício 9.1

# Carregar textura
try:
    texture = pygame.image.load("textura.jpg").convert()
    texture = pygame.transform.scale(texture, (512, 512))  
except:
    # Criar uma textura padrão se não encontrar a imagem
    texture = pygame.Surface((512, 512))
    for y in range(512):
        for x in range(512):
            texture.set_at((x, y), (x % 256, y % 256, (x + y) % 256))

# Parâmetros da esfera
sphere_radius = 150
rotation_x, rotation_y = 0, 0
texture_scale = 1.0
texture_offset_x, texture_offset_y = 0, 0
slices = 50  # Número de fatias 
stacks = 50   # Número de camadas 

def draw_sphere():
    # Criar superfície temporária para a esfera
    sphere_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for i in range(stacks):
        phi1 = math.pi * i / stacks
        phi2 = math.pi * (i + 1) / stacks
        
        for j in range(slices):
            theta1 = 2 * math.pi * j / slices
            theta2 = 2 * math.pi * (j + 1) / slices
            
            # Coordenadas 3D dos vértices
            def get_vertex(phi, theta):
                x = sphere_radius * math.sin(phi) * math.cos(theta)
                y = sphere_radius * math.sin(phi) * math.sin(theta)
                z = sphere_radius * math.cos(phi)
                
                # Rotação em X
                y_rot = y * math.cos(rotation_x) - z * math.sin(rotation_x)
                z_rot = y * math.sin(rotation_x) + z * math.cos(rotation_x)
                # Rotação em Y
                x_rot = x * math.cos(rotation_y) + z_rot * math.sin(rotation_y)
                z_rot = -x * math.sin(rotation_y) + z_rot * math.cos(rotation_y)
                
                return x_rot, y_rot, z_rot
            
            # Obter vértices rotacionados
            x0, y0, z0 = get_vertex(phi1, theta1)
            x1, y1, z1 = get_vertex(phi1, theta2)
            x2, y2, z2 = get_vertex(phi2, theta2)
            x3, y3, z3 = get_vertex(phi2, theta1)
            
            # Projeção perspectiva
            def project(x, y, z):
                focal = 500
                scale = focal / (focal + z)
                px = width // 2 + int(x * scale)
                py = height // 2 + int(y * scale)
                return px, py
            
            px0, py0 = project(x0, y0, z0)
            px1, py1 = project(x1, y1, z1)
            px2, py2 = project(x2, y2, z2)
            px3, py3 = project(x3, y3, z3)
            
            # Coordenadas de textura com ajustes de escala e offset
            def get_tex_coords(i, j):
                u = (j / slices) * texture_scale + texture_offset_x
                v = (i / stacks) * texture_scale + texture_offset_y
                return u % 1.0, v % 1.0  
            
            uv0 = get_tex_coords(i, j)
            uv1 = get_tex_coords(i, j+1)
            uv2 = get_tex_coords(i+1, j+1)
            uv3 = get_tex_coords(i+1, j)
            
            # Desenhar dois triângulos por segmento
            draw_textured_triangle(sphere_surface, 
                                 [px0, py0, px1, py1, px2, py2],
                                 [uv0, uv1, uv2])
            draw_textured_triangle(sphere_surface,
                                 [px0, py0, px2, py2, px3, py3],
                                 [uv0, uv2, uv3])
    
    screen.blit(sphere_surface, (0, 0))

def draw_textured_triangle(surface, points, tex_coords):
    # Extrair coordenadas dos pontos
    x0, y0, x1, y1, x2, y2 = points
    
    # Determinar retângulo delimitador
    min_x = max(0, min(x0, x1, x2))
    max_x = min(width, max(x0, x1, x2))
    min_y = max(0, min(y0, y1, y2))
    max_y = min(height, max(y0, y1, y2))
    
    if max_x <= min_x or max_y <= min_y:
        return
    
    # Criar máscara para o triângulo
    mask = pygame.Surface((max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA)
    pygame.draw.polygon(mask, (255, 255, 255, 255), 
                       [(x0-min_x, y0-min_y), (x1-min_x, y1-min_y), (x2-min_x, y2-min_y)])
    
    # Texturizar
    for y in range(int(min_y), int(max_y) + 1):
        for x in range(int(min_x), int(max_x) + 1):
            if mask.get_at((x - min_x, y - min_y))[3] > 0:
                # Coordenadas baricêntricas
                denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)
                if denom == 0:
                    continue
                
                a = ((y1 - y2)*(x - x2) + (x2 - x1)*(y - y2)) / denom
                b = ((y2 - y0)*(x - x2) + (x0 - x2)*(y - y2)) / denom
                c = 1 - a - b
                
                if a >= 0 and b >= 0 and c >= 0:
                    # Interpolar coordenadas de textura
                    u = a*tex_coords[0][0] + b*tex_coords[1][0] + c*tex_coords[2][0]
                    v = a*tex_coords[0][1] + b*tex_coords[1][1] + c*tex_coords[2][1]
                    
                    # Obter cor da textura
                    tex_x = int(u * texture.get_width()) % texture.get_width()
                    tex_y = int(v * texture.get_height()) % texture.get_height()
                    color = texture.get_at((tex_x, tex_y))
                    
                    surface.set_at((x, y), color)

## Exercício 9.2

# Janela de recorte
view_x1, view_y1 = 200, 150
view_x2, view_y2 = 600, 450

# Cohen-Sutherland
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def compute_code(x, y):
    code = INSIDE
    if x < view_x1: code |= LEFT
    elif x > view_x2: code |= RIGHT
    if y < view_y1: code |= TOP
    elif y > view_y2: code |= BOTTOM
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    accept = False
    
    while True:
        if not (code1 | code2):
            accept = True
            break
        elif code1 & code2:
            break
        else:
            code_out = code1 if code1 else code2
            
            if code_out & TOP:
                x = x1 + (x2 - x1) * (view_y1 - y1) / (y2 - y1)
                y = view_y1
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (view_y2 - y1) / (y2 - y1)
                y = view_y2
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (view_x2 - x1) / (x2 - x1)
                x = view_x2
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (view_x1 - x1) / (x2 - x1)
                x = view_x1
            
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)
    
    if accept:
        return (int(x1), int(y1), int(x2), int(y2))
    return None

# Linhas para recortar
lines = [
    (100, 100, 700, 500),
    (300, 50, 400, 550),
    (50, 300, 750, 300),
    (150, 500, 650, 100),
    (100, 400, 300, 200),
    (500, 100, 500, 500),
    (50, 50, 750, 550)
]

def draw_line_clipping():
    # Desenhar janela de visualização
    pygame.draw.rect(screen, WHITE, (view_x1, view_y1, view_x2 - view_x1, view_y2 - view_y1), 1)
    
    # Desenhar linhas originais
    for line in lines:
        pygame.draw.line(screen, RED, (line[0], line[1]), (line[2], line[3]), 1)
    
    # Recortar e desenhar linhas visíveis
    for line in lines:
        clipped = cohen_sutherland_clip(*line)
        if clipped:
            pygame.draw.line(screen, GREEN, (clipped[0], clipped[1]), (clipped[2], clipped[3]), 2)

# Loop Principal 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                current_exercise = 1
            elif event.key == pygame.K_2:
                current_exercise = 2
    
    screen.fill(BLACK)
    
    if current_exercise == 1:
        # Controles da esfera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: rotation_y -= 0.02
        if keys[pygame.K_RIGHT]: rotation_y += 0.02
        if keys[pygame.K_UP]: rotation_x -= 0.02
        if keys[pygame.K_DOWN]: rotation_x += 0.02
        if keys[pygame.K_q]: texture_scale *= 1.02
        if keys[pygame.K_a]: texture_scale /= 1.02
        if keys[pygame.K_w]: texture_offset_x += 0.01
        if keys[pygame.K_s]: texture_offset_x -= 0.01
        if keys[pygame.K_e]: texture_offset_y += 0.01
        if keys[pygame.K_d]: texture_offset_y -= 0.01
        
        draw_sphere()
        
        # Instruções
        font = pygame.font.SysFont('Arial', 16)
        texts = [
            "Exercício 9.1 - Mapeamento de Textura em Esfera",
            "Setas: Rotacionar esfera",
            "Q/A: Escala da textura",
            "W/S: Deslocar textura em X",
            "E/D: Deslocar textura em Y",
            "Pressione 2 para Exercício 9.2"
        ]
        for i, text in enumerate(texts):
            screen.blit(font.render(text, True, WHITE), (10, 10 + i * 20))
    
    elif current_exercise == 2:
        draw_line_clipping()
        
        # Instruções
        font = pygame.font.SysFont('Arial', 16)
        texts = [
            "Exercício 9.2 - Recorte de Linhas (Cohen-Sutherland)",
            "Vermelho: Linhas originais",
            "Verde: Linhas recortadas",
            "Pressione 1 para Exercício 9.1"
        ]
        for i, text in enumerate(texts):
            screen.blit(font.render(text, True, WHITE), (10, 10 + i * 20))
    
    pygame.display.flip()
    clock.tick(30)  

pygame.quit()
sys.exit()