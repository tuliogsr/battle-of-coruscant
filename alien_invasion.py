import pygame
import sys
import json
from pygame.sprite import Group
from Configs.settings import Settings
from Recorde.game_stats import GameStats
from Recorde.scoreboard import Scoreboard
from Configs.button import Button
from Construindo.ship import Ship
from Configs.game_functions import GameFunctions as gf
import os

class AlienInvasion:
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        # Centralize the game window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.ai_settings.screen_width, self.ai_settings.screen_height))
        pygame.display.set_caption("Battle of Coruscant")
        
        # Make the Play button.
        self.play_button = Button(self.ai_settings, self.screen, "Play")
        
        # Create an instance to store game statistics, and a scoreboard.
        self.stats = GameStats(self.ai_settings)
        self.stats.load_high_score()
        self.sb = Scoreboard(self.ai_settings, self.screen, self.stats)
        
        # Make a ship, a group of bullets, and a group of aliens.
        self.ship = Ship(self.ai_settings, self.screen)
        self.bullets = Group()
        self.aliens = Group()
        
        # Create the fleet of aliens.
        gf.create_fleet(self.ai_settings, self.screen, self.ship, self.aliens)

        self.background_image = pygame.image.load('Assents/background.png')

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            gf.check_events(self.ai_settings, self.screen, self.stats, self.sb, self.play_button, self.ship, self.aliens, self.bullets)
            
            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets)
                gf.update_aliens(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets)
            
            gf.update_screen(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets, self.play_button)

            if not self.stats.game_active and self.stats.score > 0:
                gf.save_score(self.stats.nickname, self.stats.score)
                self.show_end_screen()

    def show_end_screen(self):
        """Show the end screen with the option to return to the main menu."""
        # Desenhar o texto "Fim de Jogo"
        font = pygame.font.Font(None, 74)
        text = font.render("Fim de Jogo", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.ai_settings.screen_width // 2, self.ai_settings.screen_height // 2 - 50))
        self.screen.blit(text, text_rect)

        # Configurações do botão
        button_font = pygame.font.Font(None, 50)
        button_text = button_font.render("Voltar ao Menu", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(self.ai_settings.screen_width // 2, self.ai_settings.screen_height // 2 + 50))
        
        # Cor do botão
        button_color = (255, 165, 0)  
        # Desenhar o retângulo de fundo do botão
        pygame.draw.rect(self.screen, button_color, button_rect.inflate(20, 10))  # Inflate para ajustar o tamanho do retângulo

        # Renderizar o texto do botão sobre o retângulo
        self.screen.blit(button_text, button_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False
                        main_menu = MainMenu()
                        main_menu.run()

class MainMenu:
    def __init__(self):
        pygame.init()
        
        # Configurações de tela
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Battle of Coruscant - Menu Principal")
        
        #Background
        self.bg_image = pygame.image.load('Assents/coruscant.png')
        self.bg = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        
        # Background para a tela de recordes
        self.high_scores_bg_image = pygame.image.load('Assents/high_scores_bg.bmp')
        self.high_scores_bg = pygame.transform.scale(self.high_scores_bg_image, (self.screen_width, self.screen_height))
        
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
        self.input_box = pygame.Rect(self.screen_width // 2 - 200, self.screen_height // 2 - 50, 400, 40)
        self.start_button = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 40, 300, 50)
        self.high_score_button = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 120, 300, 50)
        self.exit_button = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 200, 300, 50)
        
        # Configuração da caixa de entrada do nickname
        self.input_text = ""
        self.input_active = False
        self.placeholder = "Digite seu Nickname"
        
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
                warning_text = "Digite seu Nickname!"
                text_surface = self.warning_font.render(warning_text, True, self.RED)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.input_box.y - 20))
                self.screen.blit(text_surface, text_rect)
            else:
                self.show_warning = False
    
    def draw_input_box(self):

        self.input_box.height = 50
        border_color = self.RED if self.show_warning else self.WHITE
        pygame.draw.rect(self.screen, border_color, self.input_box, border_radius=30)
        
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
        file_name = "Dados/player_scores.json"
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
        ai = AlienInvasion()
        ai.stats.nickname = self.input_text.strip()
        ai.run_game()
        return ai.stats.score
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            
            self.screen.blit(self.bg, (0, 0))
            
            # Desenhar o título centralizado
            self.draw_outlined_text("Battle of Coruscant", self.title_font, self.ORANGE, self.BLACK, 
                                  self.screen, self.title_x, self.title_y)
            
            self.draw_input_box()
            self.draw_button("Iniciar Jogo", self.start_button, self.ORANGE)
            self.draw_button("Recordes", self.high_score_button, self.ORANGE)
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

                    elif self.high_score_button.collidepoint(event.pos):
                        high_scores = []
                        try:
                            with open("Dados/player_scores.json", "r") as file:
                                data = json.load(file)
                                for name, score in data.items():
                                    high_scores.append((name, score))
                        except (FileNotFoundError, json.JSONDecodeError):
                            pass
                        
                        high_scores.sort(key=lambda x: x[1], reverse=True)
                        
                        self.screen.blit(self.high_scores_bg, (0, 0))  # Exibir a imagem de fundo
                        self.draw_text("Recordes", self.title_font, self.ORANGE, self.screen, self.screen_width // 2, 50)
                        y = 150  # Aumentar o espaço inicial
                        for i, (name, score) in enumerate(high_scores[:5], 1):  # Mostrar apenas os 5 melhores
                            text = f"{i}. {name}: {score}"
                            text_surface = self.button_font.render(text, True, self.WHITE)
                            text_rect = text_surface.get_rect(center=(self.screen_width // 2, y))
                            self.screen.blit(text_surface, text_rect)
                            y += 70  # Aumentar o espaço entre cada usuário
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        self.screen.blit(self.bg, (0, 0))

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
