import pygame
from pygame.sprite import Sprite

class GameObject(Sprite):
    """Classe base para objetos do jogo."""

    def __init__(self, image_path, screen):
        super(GameObject, self).__init__()
        self.screen = screen

        # Carregar a imagem e definir o rect.
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def update(self):
        """Atualiza a posição do objeto (sobrescrito em subclasses, se necessário)."""
        pass

    def blitme(self):
        """Desenha o objeto na tela em sua posição atual."""
        self.screen.blit(self.image, self.rect)