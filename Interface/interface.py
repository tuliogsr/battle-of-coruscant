import pygame
import sys
import json
from Interface.jogo_space import Game

class MainMenu:
    def __init__(self):
        pygame.init()
        
        # Configurações de tela
        self.screen_width = 960
        self.screen_height = 540
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Battle of Coruscant - Tela Inicial")
        
        # Carregar e ajustar imagem de fundo
        self.background_image = pygame.image.load("Assents/coruscant.png")
        # Preservar a proporção da imagem ao redimensionar
        img_ratio = self.background_image.get_width() / self.background_image.get_height()
        new_height = self.screen_height
        new_width = int(new_height * img_ratio)
        
        if new_width < self.screen_width:
            new_width = self.screen_width
            new_height = int(new_width / img_ratio)
            
        self.background = pygame.transform.scale(self.background_image, (new_width, new_height))
        
        # Calcular posição para centralizar a imagem
        self.bg_x = (self.screen_width - new_width) // 2
        self.bg_y = (self.screen_height - new_height) // 2
        
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
        self.placeholder = "Nickname"
        
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
                warning_text = "Digite um nickname!"
                text_surface = self.warning_font.render(warning_text, True, self.RED)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.input_box.y - 20))
                self.screen.blit(text_surface, text_rect)
            else:
                self.show_warning = False
    
    def draw_input_box(self):
        # Desenhar a caixa arredondada com borda vermelha se mostrar aviso
        border_color = self.RED if self.show_warning else self.WHITE
        pygame.draw.rect(self.screen, border_color, self.input_box, border_radius=20)
        
        # Se não há texto e a caixa não está ativa, mostrar o placeholder
        if not self.input_text and not self.input_active:
            placeholder_surface = self.input_font.render(self.placeholder, True, self.GRAY)
            placeholder_rect = placeholder_surface.get_rect(center=self.input_box.center)
            self.screen.blit(placeholder_surface, placeholder_rect)
        else:
            # Renderizar o texto dentro da caixa
            text_surface = self.input_font.render(self.input_text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=self.input_box.center)
            
            # Garantir que o texto não ultrapasse a caixa
            if text_rect.width > self.input_box.width - 20:
                text_rect.x = self.input_box.x + 10
                text_rect.y = self.input_box.y + (self.input_box.height - text_rect.height) // 2
            
            self.screen.blit(text_surface, text_rect)
            
            # Desenhar cursor quando ativo
            if self.input_active and pygame.time.get_ticks() % 1000 < 500:
                cursor_pos = text_rect.right
                if cursor_pos > self.input_box.right - 10:
                    cursor_pos = self.input_box.right - 10
                pygame.draw.line(self.screen, self.BLACK,
                               (cursor_pos, self.input_box.y + 10),
                               (cursor_pos, self.input_box.y + self.input_box.height - 10))

def save_score(self, nickname, score):
    """
    Salva o nickname do jogador e sua maior pontuação em um arquivo.
    
    Args:
        nickname (str): O nickname do jogador.
        score (int): A pontuação do jogador.
    """
    # Nome do arquivo para armazenar os dados
    file_name = "player_scores.json"
    
    try:
        # Tentar carregar os dados existentes
        with open(file_name, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Caso o arquivo não exista ou esteja corrompido, criar um novo dicionário
        data = {}
    
    # Atualizar ou adicionar o recorde do jogador
    if nickname in data:
        # Salvar apenas se a nova pontuação for maior
        if score > data[nickname]:
            data[nickname] = score
    else:
        # Adicionar novo jogador
        data[nickname] = score
    
    # Salvar os dados atualizados no arquivo
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Pontuação salva: {nickname} - {score}")
    
    def run(self):
        while True:
            # Desenhar o fundo
            self.screen.blit(self.background, (self.bg_x, self.bg_y))
            
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
                            game = Game()
                            game.start()
                            if self.input_text.strip():
                                game = Game()
                                final_score = game.start()  # Modifique o método `start` para retornar a pontuação final.
                                self.save_score(self.input_text.strip(), final_score)  # Salvar o nickname e a pontuação.
                            else:
                                self.show_warning = True
                                self.warning_timer = pygame.time.get_ticks()
                        else:
                            self.show_warning = True
                            self.warning_timer = pygame.time.get_ticks()
                    elif self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        print(f"Nickname: {self.input_text}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 15:
                            self.input_text += event.unicode
            
            pygame.display.flip()