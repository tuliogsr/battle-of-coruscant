'''
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Battle of Coruscant")
    
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

import pygame
import sys
import json
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

class MainMenu:
    def __init__(self):
        pygame.init()
        
        # Configurações de tela
        self.screen_width = 920
        self.screen_height = 540
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Battle of Coruscant - Menu Principal")
        
        # Definir cores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.ORANGE = (255, 69, 0)
        self.GRAY = (169, 169, 169)
        self.RED = (255, 0, 0)
        
        # Configurações de fonte
        self.title_font = pygame.font.Font(None, 90)  
        self.button_font = pygame.font.Font(None, 50)
        self.input_font = pygame.font.Font(None, 40)
        self.warning_font = pygame.font.Font(None, 36)
        
        # Titulo do jogo
        title_text = "Battle of Coruscant"
        title_surface = self.title_font.render(title_text, True, self.ORANGE)
        title_width = title_surface.get_width()
        self.title_x = (self.screen_width - title_width) // 2
        self.title_y = self.screen_height // 4
        
        # Definir posições dos botões
        self.input_box = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 50, 300, 40)
        self.start_button = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 120, 300, 50)
        self.exit_button = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 200, 300, 50)
        
        # Configuração da caixa de entrada do nickname
        self.input_text = ""
        self.input_active = False
        self.placeholder = "Digite seu nome"
        
        # Configuração do aviso
        self.show_warning = False
        self.warning_timer = 0
        self.warning_duration = 2000  # 2 segundos

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
        self.draw_text(text, self.button_font, self.BLACK, self.screen, 
                      button_rect.x + button_rect.width // 2, 
                      button_rect.y + button_rect.height // 2)
    
    def draw_warning(self):
        if self.show_warning:
            current_time = pygame.time.get_ticks()
            if current_time - self.warning_timer < self.warning_duration:
                warning_text = "Digite seu nome para começar!"
                text_surface = self.warning_font.render(warning_text, True, self.RED)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.input_box.y - 20))
                self.screen.blit(text_surface, text_rect)
            else:
                self.show_warning = False
    
    def draw_input_box(self):
        border_color = self.RED if self.show_warning else self.WHITE
        pygame.draw.rect(self.screen, border_color, self.input_box, border_radius=20)
        
        if not self.input_text and not self.input_active:
            placeholder_surface = self.input_font.render(self.placeholder, True, self.GRAY)
            placeholder_rect = placeholder_surface.get_rect(center=self.input_box.center)
            self.screen.blit(placeholder_surface, placeholder_rect)
        else:
            text_surface = self.input_font.render(self.input_text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=self.input_box.center)
            
            if text_rect.width > self.input_box.width - 20:
                text_rect.x = self.input_box.x + 10
                text_rect.y = self.input_box.y + (self.input_box.height - text_rect.height) // 2
            
            self.screen.blit(text_surface, text_rect)
            
            if self.input_active and pygame.time.get_ticks() % 1000 < 500:
                cursor_pos = text_rect.right
                if cursor_pos > self.input_box.right - 10:
                    cursor_pos = self.input_box.right - 10
                pygame.draw.line(self.screen, self.BLACK,
                               (cursor_pos, self.input_box.y + 10),
                               (cursor_pos, self.input_box.y + self.input_box.height - 10))

    def save_score(self, nickname, score):
        file_name = "player_scores.json"
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        if nickname in data:
            if score > data[nickname]:
                data[nickname] = score
        else:
            data[nickname] = score
        
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    def start_game(self):
        # Initialize game components
        ai_settings = Settings()
        screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        pygame.display.set_caption("Battle of Coruscant")
        
        play_button = Button(ai_settings, screen, "Play")
        stats = GameStats(ai_settings)
        sb = Scoreboard(ai_settings, screen, stats)
        ship = Ship(ai_settings, screen)
        bullets = Group()
        aliens = Group()
        
        gf.create_fleet(ai_settings, screen, ship, aliens)
        
        # Game loop
        while True:
            gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
            
            if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
            
            # Se o jogo terminar, retornar a pontuação
            if not stats.game_active and not stats.ships_left:
                return stats.score
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            self.screen.fill(self.BLACK)
            
            # Desenhar o título centralizado
            self.draw_outlined_text("Battle of Coruscant", self.title_font, self.ORANGE, self.BLACK, 
                                  self.screen, self.title_x, self.title_y)
            
            self.draw_input_box()
            self.draw_button("Iniciar Jogo", self.start_button, self.ORANGE)
            self.draw_button("Sair", self.exit_button, self.ORANGE)
            self.draw_warning()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                        
                    if self.start_button.collidepoint(event.pos):
                        if self.input_text.strip():
                            final_score = self.start_game()
                            self.save_score(self.input_text.strip(), final_score)
                        else:
                            self.show_warning = True
                            self.warning_timer = pygame.time.get_ticks()
                    elif self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            final_score = self.start_game()
                            self.save_score(self.input_text.strip(), final_score)
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 15:
                            self.input_text += event.unicode
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    menu = MainMenu()
    menu.run()