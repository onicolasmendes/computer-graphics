# Nicolas Expedito Lana Mendes 22.1.4028

import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atividade 8: Iluminação, Fontes de Luz e Transparência")
clock = pygame.time.Clock()

# Modo de execução: 1 = Iluminação , 2 = Fontes de Luz, 3 = Transparência
mode = 1

# Parâmetros da fonte de luz: posição, tipo e ângulo para spotlight
light_pos = [0, 0, 200]
light_type = "point"
spot_cutoff = math.radians(30)

# normalização e produto escalar
def normalize(v):
    x, y, z = v
    mag = math.sqrt(x*x + y*y + z*z)
    return (x/mag, y/mag, z/mag) if mag != 0 else (0,0,0)

def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

# Exercicio 8.1

# Especificações da esfera e material para Phong
sphere_center = (WIDTH//2, HEIGHT//2 - 50)
sphere_radius = 100
material8_1 = {"ka": 0.1, "kd": 0.7, "ks": 0.2, "alpha": 10, "color": (200,100,100)}

# Iluminação Phong: ambiente + difusa + especular
def phong_shading(N, L, V, material):
    Ia = material["ka"]
    Id = material["kd"] * max(dot(N,L), 0)
    R_vec = normalize((2 * max(dot(N,L), 0) * N[0] - L[0],
                       2 * max(dot(N,L), 0) * N[1] - L[1],
                       2 * max(dot(N,L), 0) * N[2] - L[2]))
    Is = material["ks"] * (max(dot(R_vec,V), 0) ** material["alpha"])
    return Ia + Id + Is

# Renderização da esfera iluminada pixel a pixel
def render_sphere_8_1():
    R = sphere_radius
    surf = pygame.Surface((2*R,2*R))
    for y in range(2*R):
        for x in range(2*R):
            lx, ly = x - R, y - R
            if lx*lx + ly*ly <= R*R:
                lz = math.sqrt(R*R - lx*lx - ly*ly)
                N = normalize((lx, ly, lz))
                L = normalize((light_pos[0]-lx, light_pos[1]-ly, light_pos[2]-lz))
                V = (0,0,1)
                intensity = min(phong_shading(N, L, V, material8_1), 1)
                r, g, b = [min(255, int(c * intensity)) for c in material8_1["color"]]
                surf.set_at((x,y), (r,g,b))
            else:
                surf.set_at((x,y), (0,0,0))
    return surf

# Iluminação do plano com normal fixa
def render_plane():
    base = (100,100,100)
    N = (0,1,0)
    L = normalize(light_pos)
    diff = max(dot(N,L), 0)
    intensity = 0.2 + 0.8*diff
    return tuple(min(255, int(c * intensity)) for c in base)

# Desenha a cena do exercício 8.1
def render_ex8_1():
    screen.fill((30,30,50))
    pygame.draw.rect(screen, render_plane(), (0, HEIGHT//2+100, WIDTH, HEIGHT//2))
    screen.blit(render_sphere_8_1(), (sphere_center[0] - sphere_radius, sphere_center[1] - sphere_radius))
    pygame.draw.circle(screen, (255,255,0), (sphere_center[0] + light_pos[0], sphere_center[1] + light_pos[1]), 5)
    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Ex 8.1: Use setas e Q/E para mover a luz", True, (255,255,255)), (10,10))

# Exercicio 8.2

# Parâmetros do material para a esfera do exercício 8.2
cube_material = {"ka": 0.1, "kd": 0.6, "ks": 0.3, "alpha": 20, "color": (150,150,255)}

# Renderiza a esfera com iluminação baseada no tipo de luz selecionado
def render_sphere_8_2():
    R = sphere_radius
    surf = pygame.Surface((2*R, 2*R))
    for y in range(2*R):
        for x in range(2*R):
            lx, ly = x - R, y - R
            if lx*lx + ly*ly <= R*R:
                lz = math.sqrt(R*R - lx*lx - ly*ly)
                N = normalize((lx, ly, lz))

                # Calcula direção da luz dependendo do tipo
                if light_type == "point":
                    L = normalize((light_pos[0]-lx, light_pos[1]-ly, light_pos[2]-lz))
                elif light_type == "directional":
                    L = normalize((-light_pos[0], -light_pos[1], -light_pos[2]))
                elif light_type == "spot":
                    L = normalize((light_pos[0]-lx, light_pos[1]-ly, light_pos[2]-lz))
                    angle = math.acos(dot(L, normalize((0,0,-1))))
                    if angle > spot_cutoff:
                        intensity = cube_material["ka"]
                        color = [int(c * intensity) for c in cube_material["color"]]
                        surf.set_at((x,y), tuple(color))
                        continue

                V = (0,0,1)
                Ia = cube_material["ka"]
                Id = cube_material["kd"] * max(dot(N,L), 0)
                R_vec = normalize((2*max(dot(N,L),0)*N[0]-L[0],
                                   2*max(dot(N,L),0)*N[1]-L[1],
                                   2*max(dot(N,L),0)*N[2]-L[2]))
                Is = cube_material["ks"] * (max(dot(R_vec,V), 0) ** cube_material["alpha"])
                intensity = min(Ia + Id + Is, 1)
                color = [min(255, int(c * intensity)) for c in cube_material["color"]]
                surf.set_at((x,y), tuple(color))
            else:
                surf.set_at((x,y), (0,0,0))
    return surf

# Renderiza a cena do exercício 8.2
def render_ex8_2():
    screen.fill((50,50,50))
    screen.blit(render_sphere_8_2(), (sphere_center[0] - sphere_radius, sphere_center[1] - sphere_radius))
    pygame.draw.circle(screen, (255,255,0), (sphere_center[0] + light_pos[0], sphere_center[1] + light_pos[1]), 5)
    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Ex 8.2: Setas/QE movem luz | O/P mudam cutoff | L troca tipo", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Tipo: {light_type} | Cutoff: {math.degrees(spot_cutoff):.1f}°", True, (255,255,255)), (10,40))

# Exercicio 8.3

# Lista de objetos com posição, cor e alfa
objects = [
    {"pos": (100,100), "size": (200,200), "color": (255,0,0), "alpha":150},
    {"pos": (150,150), "size": (200,200), "color": (0,255,0), "alpha":100},
    {"pos": (200,200), "size": (200,200), "color": (0,0,255), "alpha":200}
]
selected_obj = 0

# Renderiza os objetos transparentes
def render_ex8_3():
    screen.fill((20,20,20))
    for obj in objects:
        surf = pygame.Surface(obj["size"], pygame.SRCALPHA)
        surf.fill((*obj["color"], obj["alpha"]))
        screen.blit(surf, obj["pos"])
    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Ex 8.3: Teclas 4-6 selecionam | Q/A alteram transparência", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Objeto: {selected_obj+1} | Alpha: {objects[selected_obj]['alpha']}", True, (255,255,255)), (10,40))

# Atualiza transparência do objeto selecionado
def update_ex8_3():
    global selected_obj
    keys = pygame.key.get_pressed()
    if keys[pygame.K_4]: selected_obj = 0
    if keys[pygame.K_5]: selected_obj = 1
    if keys[pygame.K_6]: selected_obj = 2
    if keys[pygame.K_q]: objects[selected_obj]["alpha"] = min(255, objects[selected_obj]["alpha"] + 2)
    if keys[pygame.K_a]: objects[selected_obj]["alpha"] = max(0, objects[selected_obj]["alpha"] - 2)

# Controles

# Movimentação da fonte de luz
def update_light():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: light_pos[0] -= 2
    if keys[pygame.K_RIGHT]: light_pos[0] += 2
    if keys[pygame.K_UP]: light_pos[1] -= 2
    if keys[pygame.K_DOWN]: light_pos[1] += 2
    if keys[pygame.K_q]: light_pos[2] -= 2
    if keys[pygame.K_e]: light_pos[2] += 2

# Ajuste do cutoff da spotlight
def update_spot_cutoff():
    global spot_cutoff
    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]: spot_cutoff = max(math.radians(5), spot_cutoff - math.radians(1))
    if keys[pygame.K_p]: spot_cutoff = min(math.radians(90), spot_cutoff + math.radians(1))

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: mode = 1
            elif event.key == pygame.K_2: mode = 2
            elif event.key == pygame.K_3: mode = 3
            elif mode == 2 and event.key == pygame.K_l:
                light_type = {"point":"directional", "directional":"spot", "spot":"point"}[light_type]

    if mode in [1, 2]: update_light()
    if mode == 2: update_spot_cutoff()
    if mode == 3: update_ex8_3()

    if mode == 1: render_ex8_1()
    elif mode == 2: render_ex8_2()
    elif mode == 3: render_ex8_3()

    pygame.display.flip()
    clock.tick(30)