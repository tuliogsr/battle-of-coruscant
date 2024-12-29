# jogo.py
import pygame
import sys

class Game:
    def __init__(self):
        # Configurações do jogo
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Battle of Coruscant - Jogo")
        
        # Carregar elementos específicos do jogo (por exemplo, plano de fundo, personagens, etc.)
        self.background_color = (255, 69, 0)  # Altere para a cor ou imagem desejada

    def start(self):
        # Loop principal do jogo
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Lógica do jogo aqui
            self.screen.fill(self.background_color)  # Exemplo: fundo do jogo
            # Adicione outras partes da lógica do jogo
            
            pygame.display.flip()
