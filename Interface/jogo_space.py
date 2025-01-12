import pygame
from pygame.sprite import Group

from Auxiliar.settings import Settings
from Auxiliar.game_stats import GameStats
from Auxiliar.scoreboard import Scoreboard
from Auxiliar.button import Button
from Auxiliar.ship import Ship
import Auxiliar.game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Set the background color.
    bg_color = (230, 230, 230)
    
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
            bullets, play_button)

run_game()



'''
# jogo.py
import pygame
import sys
import Interface.jogo_space as jogo_space

class Game:
    def __init__(self):
        # Configurações do jogo
        self.screen_width = 960
        self.screen_height = 540
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
'''