import pygame
import sys
from src.Interface.jogo_space import Game
# Importa a classe Game do arquivo jogo.py

class MainMenu:
    def __init__(self):
        # Inicializar o Pygame
        pygame.init()
        
        # Configurações de tela
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Battle of Coruscant - Tela Inicial")
        
        # Carregar imagem de fundo e ajustar ao tamanho da tela
        self.background_image = pygame.image.load("coruscant.png")
        self.background = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        # Definir cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.ORANGE = (255, 69, 0)
        
        # Configurações de fonte
        self.title_font = pygame.font.Font(None, 150)
        self.button_font = pygame.font.Font(None, 50)
        
        # Definir posições dos botões
        self.start_button = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2, 300, 50)
        self.exit_button = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 + 100, 300, 50)
    
    def draw_outlined_text(self, text, font, text_color, outline_color, surface, x, y):
        outline_width = 2
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    outline_text = font.render(text, True, outline_color)
                    surface.blit(outline_text, (x + dx, y + dy))
        
        text_surface = font.render(text, True, text_color)
        surface.blit(text_surface, (x, y))
    
    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)
    
    def draw_button(self, text, button_rect, color):
        pygame.draw.rect(self.screen, color, button_rect)
        self.draw_text(text, self.button_font, self.BLACK, self.screen, button_rect.x + button_rect.width // 2, button_rect.y + button_rect.height // 2)
    
    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            self.draw_outlined_text("Battle of Coruscant", self.title_font, self.ORANGE, self.BLACK, self.screen, self.screen_width // 2 - 480, self.screen_height // 4)
            self.draw_button("Iniciar Jogo", self.start_button, self.ORANGE)
            self.draw_button("Sair", self.exit_button, self.ORANGE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        game = Game()  # Cria uma instância de Game
                        game.start()   # Inicia o jogo
                    elif self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.flip()
