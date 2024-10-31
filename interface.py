import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações de tela
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle of Coruscant - Tela Inicial")

# Carregar imagem de fundo
background_image = pygame.image.load("coruscant.png")
background = pygame.transform.scale(background_image, (screen_width, screen_height))  # Ajusta a imagem ao tamanho da tela

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 69 ,0)
BLUE = (0, 0, 255)

# Configurações de fonte
font = pygame.font.Font(None, 150)  # Título
button_font = pygame.font.Font(None, 50)  # Texto dos botões

def draw_outlined_text(text, font, text_color, outline_color, surface, x, y):
    # Desenha o contorno ao redor (um pouco deslocado em cada direção)
    outline_width = 2  # Largura do contorno
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                surface.blit(outline_text, (x + dx, y + dy))
    # Desenha o texto preenchido no centro do contorno
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (x, y))

# Função para mostrar texto na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Função para desenhar botões
def draw_button(text, x, y, w, h, color, font):
    pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, font, BLACK, screen, x + w // 2, y + h // 2)

# Loop principal para a tela inicial
def main_menu():
    while True:
        screen.blit(background_image, (0, 0))
        
        # Título
        draw_outlined_text("Battle of Coruscant", font, ORANGE, BLACK, screen, screen_width // 2 - 480, screen_height // 4)
        
        # Botões
        start_button = pygame.Rect(screen_width // 2 - 140, screen_height // 2, 300, 50)
        exit_button = pygame.Rect(screen_width // 2 - 140, screen_height // 2 + 100, 300, 50)
        
        draw_button("Iniciar Jogo", start_button.x, start_button.y, start_button.width, start_button.height, ORANGE, button_font)
        draw_button("Sair", exit_button.x, exit_button.y, exit_button.width, exit_button.height, ORANGE, button_font)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    # Aqui você colocaria a função que inicia o jogo
                    print("Iniciar Jogo")
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()

# Executa o menu inicial
main_menu()