import pygame.font

class Button:
    def __init__(self, ai_settings, screen, msg):
        """Inicializa os atributos do botão."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Define as dimensões e propriedades do botão.
        self.width, self.height = 200, 50  # Largura e altura do botão.
        self.button_color = (0, 255, 0)  # Cor do botão (verde).
        self.text_color = (255, 255, 255)  # Cor do texto (branco).
        self.font = pygame.font.SysFont(None, 48)  # Fonte e tamanho do texto.
        
        # Constrói o objeto 'rect' do botão e centraliza-o na tela.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # A mensagem do botão precisa ser preparada apenas uma vez.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Transforma a mensagem em uma imagem renderizada e centraliza o texto no botão."""
        # Renderiza a mensagem em uma imagem com as cores definidas.
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # Obtém o retângulo da imagem do texto e centraliza-o no botão.
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """Desenha o botão em branco e, em seguida, desenha a mensagem."""
        # Preenche a área do botão com a cor definida.
        self.screen.fill(self.button_color, self.rect)
        # Desenha a imagem do texto sobre o botão.
        self.screen.blit(self.msg_image, self.msg_image_rect)
