import pygame

class Laser:
    def __init__(self, x, y, largura, altura, cor, velocidade):
        """Inicializa um projétil."""
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
        self.velocidade = velocidade
    
    def desenhar(self, tela):
        """Desenha o projétil na tela."""
        pygame.draw.rect(tela, self.cor, self.rect)
    
    def mover(self):
        """Move o projétil."""
        self.rect.y += self.velocidade
