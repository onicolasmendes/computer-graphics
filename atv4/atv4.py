# Nicolas Expedito Lana Mendes 22.1.4028
import pygame
import sys
import math
import colorsys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atividade 4: Teoria das Cores")
clock = pygame.time.Clock()

mode = 1

# Fonte para exibição de textos
font = pygame.font.SysFont(None, 30)

# Variáveis para entrada de dados no Exercício 2 
active_field = 0  # 0: valor R, 1: valor G, 2: valor B
input_R = ""
input_G = ""
input_B = ""

def draw_gradient():
    # Exercício 1: Gradiente onde o componente R varia de 0 a 255, enquanto G e B permanecem constantes 
    for x in range(WIDTH):
        r = int((x / WIDTH) * 255)
        color = (r, 128, 128)
        pygame.draw.line(screen, color, (x, 0), (x, HEIGHT))

def draw_rgb_to_hsv():
    global input_R, input_G, input_B
    # Exibe os campos de entrada para R, G e B
    label_R = font.render("Digite o valor de R (0-255): " + input_R, True, (255, 255, 255))
    label_G = font.render("Digite o valor de G (0-255): " + input_G, True, (255, 255, 255))
    label_B = font.render("Digite o valor de B (0-255): " + input_B, True, (255, 255, 255))
    screen.blit(label_R, (50, 100))
    screen.blit(label_G, (50, 150))
    screen.blit(label_B, (50, 200))
    
    # Quando os três valores forem digitados, realiza a conversão para HSV
    if input_R != "" and input_G != "" and input_B != "":
        try:
            R = int(input_R)
            G = int(input_G)
            B = int(input_B)
            # Limita os valores ao intervalo 0-255
            R = max(0, min(R, 255))
            G = max(0, min(G, 255))
            B = max(0, min(B, 255))
            r, g, b = R/255.0, G/255.0, B/255.0
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            h_deg = h * 360
            s_perc = s * 100
            v_perc = v * 100
            result_rgb = font.render(f"RGB: ({R}, {G}, {B})", True, (255,255,255))
            result_hsv = font.render(f"HSV: ({h_deg:.1f}°, {s_perc:.1f}%, {v_perc:.1f}%)", True, (255,255,255))
            screen.blit(result_rgb, (50, 300))
            screen.blit(result_hsv, (50, 350))
        except:
            error_text = font.render("Erro na conversão dos valores.", True, (255, 0, 0))
            screen.blit(error_text, (50, 300))

def draw_rgb_to_cmyk():
    # Exercício 3: Conversão da cor fixa (255, 128, 64) do modelo RGB para CMYK
    R, G, B = 255, 128, 64
    r, g, b = R/255.0, G/255.0, B/255.0
    K = 1 - max(r, g, b)
    if K == 1:
        C = M = Y = 0
    else:
        C = (1 - r - K) / (1 - K)
        M = (1 - g - K) / (1 - K)
        Y = (1 - b - K) / (1 - K)
    C_perc = C * 100
    M_perc = M * 100
    Y_perc = Y * 100
    K_perc = K * 100
    text_rgb = font.render(f"RGB: ({R}, {G}, {B})", True, (255,255,255))
    text_cmyk = font.render(f"CMYK: ({C_perc:.1f}%, {M_perc:.1f}%, {Y_perc:.1f}%, {K_perc:.1f}%)", True, (255,255,255))
    screen.blit(text_rgb, (50, HEIGHT//2 - 40))
    screen.blit(text_cmyk, (50, HEIGHT//2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            # Alterna entre os modos: 1, 2 e 3
            if event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
                # Reinicia os campos de entrada ao mudar para o modo 2
                active_field = 0
                input_R = ""
                input_G = ""
                input_B = ""
            elif event.key == pygame.K_3:
                mode = 3
            
            # no Exercício 2, processa a entrada de dados via teclado
            if mode == 2:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == 0 and len(input_R) > 0:
                        input_R = input_R[:-1]
                    elif active_field == 1 and len(input_G) > 0:
                        input_G = input_G[:-1]
                    elif active_field == 2 and len(input_B) > 0:
                        input_B = input_B[:-1]
                elif event.key == pygame.K_RETURN:
                    # Avança para o próximo campo ao pressionar Enter
                    active_field = (active_field + 1) % 3
                elif event.unicode.isdigit():
                    if active_field == 0:
                        input_R += event.unicode
                    elif active_field == 1:
                        input_G += event.unicode
                    elif active_field == 2:
                        input_B += event.unicode

    screen.fill((0, 0, 0))
    if mode == 1:
        draw_gradient()
        text_mode = font.render("Exercício 1: Gradiente RGB (R varia, G e B constantes)", True, (255,255,255))
        screen.blit(text_mode, (20, 20))
    elif mode == 2:
        draw_rgb_to_hsv()
        text_mode = font.render("Exercício 2: Conversão RGB para HSV (Digite os valores)", True, (255,255,255))
        screen.blit(text_mode, (20, 20))
    elif mode == 3:
        draw_rgb_to_cmyk()
        text_mode = font.render("Exercício 3: Conversão RGB para CMYK", True, (255,255,255))
        screen.blit(text_mode, (20, 20))

    instructions = font.render("Pressione 1, 2 ou 3 para alternar entre os exercícios", True, (255,255,255))
    screen.blit(instructions, (20, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
