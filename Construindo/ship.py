import pygame
from pygame.sprite import Sprite
from Construindo.game_object import GameObject

class Ship(GameObject):
    """Classe para representar a nave do jogador."""

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__('Assents/ship.bmp', screen)
        self.ai_settings = ai_settings

        # Configuração inicial da nave.
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.bottom = self.screen.get_rect().bottom

        # Armazenar um valor decimal para a posição horizontal.
        self.center = float(self.rect.centerx)

        # Flags de movimento.
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Centraliza a nave na tela."""
        self.center = self.screen.get_rect().centerx

    def update(self):
        """Atualiza a posição da nave com base nas flags de movimento."""
        if self.moving_right and self.rect.right < self.screen.get_rect().right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Atualizar o rect com base na posição central.
        self.rect.centerx = self.center

