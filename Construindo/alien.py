from pygame.sprite import Sprite
from Construindo.game_object import GameObject

class Alien(GameObject):
    """Classe para representar um alienígena."""

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__('Assents/alien.bmp', screen)
        self.ai_settings = ai_settings

        # Posição inicial do alienígena.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazenar a posição exata do alienígena.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Retorna True se o alien estiver na borda da tela."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """Move o alienígena para a direita ou para a esquerda."""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

