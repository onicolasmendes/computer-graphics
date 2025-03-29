# Nicolas Expedito Lana Mendes 22.1.4028
import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atividade 6: Robô e Sistema Solar")
clock = pygame.time.Clock()

mode = 1

# Variáveis para Exercício 1: Robô com Braço Animado
# Centro do robô posição do corpo
robot_center = (WIDTH // 2, HEIGHT // 2)
# Parâmetros do corpo
body_angle = 0.0       
body_speed = 0.005     
# Parâmetros do braço
arm_amplitude = math.radians(30)  
arm_length = 100                  # Comprimento do braço
arm_attachment_offset = 40        
# Parâmetros do antebraço
forearm_length = 80               # Comprimento do antebraço
forearm_offset = 0.0              # Ângulo acumulado para o antebraço
forearm_speed = 0.05             
# Variável para controlar a oscilação do braço
robot_time = 0

# Variáveis para Exercício 2: Sistema Solar Simples
sun_center = (WIDTH // 2, HEIGHT // 2)  
earth_orbit_radius = 200                
moon_orbit_radius = 50                 
earth_angle = 0.0                       
moon_angle = 0.0                       
earth_speed = 0.01                      
moon_speed = 0.05                     

# Cores
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
YELLOW  = (255, 255, 0)   # Sol
BLUE    = (0, 0, 255)     # Terra
GRAY    = (150, 150, 150) # Lua
RED     = (255, 0, 0)

font = pygame.font.SysFont(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #  1 para Robô e 2 para Sistema Solar
            if event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2

    screen.fill(BLACK)
    
    if mode == 1:
        # Exercício 1: Robô com Braço Animado
        # Atualiza o ângulo do corpo e a oscilação do braço
        body_angle += body_speed
        robot_time += 1
        arm_oscillation = arm_amplitude * math.sin(robot_time * 0.05)
        forearm_offset += forearm_speed

        # Calcula a posição de fixação do braço 
        base_x = robot_center[0] + arm_attachment_offset * math.cos(body_angle)
        base_y = robot_center[1] + arm_attachment_offset * math.sin(body_angle)
        arm_base = (base_x, base_y)

        # Ângulo total do braço 
        total_arm_angle = body_angle + arm_oscillation
        arm_end_x = arm_base[0] + arm_length * math.cos(total_arm_angle)
        arm_end_y = arm_base[1] + arm_length * math.sin(total_arm_angle)
        arm_end = (arm_end_x, arm_end_y)

        # O antebraço gira em relação ao braço
        total_forearm_angle = total_arm_angle + forearm_offset
        forearm_end_x = arm_end[0] + forearm_length * math.cos(total_forearm_angle)
        forearm_end_y = arm_end[1] + forearm_length * math.sin(total_forearm_angle)
        forearm_end = (forearm_end_x, forearm_end_y)

        # Desenha o corpo do robô
        pygame.draw.circle(screen, (100, 100, 255), robot_center, 40)
        # Desenha um marcador para indicar a rotação do corpo
        marker_end = (robot_center[0] + 40 * math.cos(body_angle),
                      robot_center[1] + 40 * math.sin(body_angle))
        pygame.draw.line(screen, WHITE, robot_center, marker_end, 2)

        # Desenha o braço e o antebraço
        pygame.draw.line(screen, RED, arm_base, arm_end, 4)
        pygame.draw.line(screen, (0,255,0), arm_end, forearm_end, 4)

        # Desenha os pontos de articulação
        pygame.draw.circle(screen, WHITE, (int(robot_center[0]), int(robot_center[1])), 5)
        pygame.draw.circle(screen, WHITE, (int(arm_base[0]), int(arm_base[1])), 5)
        pygame.draw.circle(screen, WHITE, (int(arm_end[0]), int(arm_end[1])), 5)

        text = font.render("Exercício 1: Robô com Braço Animado", True, WHITE)
        screen.blit(text, (20, 20))
        
    elif mode == 2:
        # Exercício 2: Sistema Solar Simples
        # Atualiza os ângulos de órbita
        earth_angle += earth_speed
        moon_angle += moon_speed

        # Calcula a posição da Terra em órbita ao redor do Sol
        earth_x = sun_center[0] + earth_orbit_radius * math.cos(earth_angle)
        earth_y = sun_center[1] + earth_orbit_radius * math.sin(earth_angle)
        earth_pos = (int(earth_x), int(earth_y))

        # Calcula a posição da Lua em órbita ao redor da Terra
        moon_x = earth_x + moon_orbit_radius * math.cos(moon_angle)
        moon_y = earth_y + moon_orbit_radius * math.sin(moon_angle)
        moon_pos = (int(moon_x), int(moon_y))

        # Desenha tudo
        pygame.draw.circle(screen, YELLOW, sun_center, 40)  # Sol
        pygame.draw.circle(screen, WHITE, sun_center, earth_orbit_radius, 1)  # Órbita da Terra
        pygame.draw.circle(screen, BLUE, earth_pos, 20)  # Terra
        pygame.draw.circle(screen, WHITE, earth_pos, moon_orbit_radius, 1)  # Órbita da Lua
        pygame.draw.circle(screen, GRAY, moon_pos, 10)  # Lua

        text = font.render("Exercício 2: Sistema Solar Simples", True, WHITE)
        screen.blit(text, (20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
