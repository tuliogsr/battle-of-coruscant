import pygame
from Construindo.Laser import Laser

class Nave:
    def __init__(self, x, y, largura, altura, cor, velocidade):
        """
        Inicializa a nave.
        
        Args:
            x (int): Posição inicial no eixo X.
            y (int): Posição inicial no eixo Y.
            largura (int): Largura da nave.
            altura (int): Altura da nave.
            cor (tuple): Cor da nave (R, G, B).
            velocidade (int): Velocidade de movimentação da nave.
        """
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.velocidade = velocidade
        self.rect = pygame.Rect(x, y, largura, altura)
    
    def desenhar(self, tela):
        """Desenha a nave na tela."""
        pygame.draw.rect(tela, self.cor, self.rect)
    
    def mover(self, direcao):
        """
        Move a nave em uma direção.
        
        Args:
            direcao (str): Direção do movimento ('esquerda', 'direita').
        """
        if direcao == 'esquerda':
            self.rect.x -= self.velocidade
        elif direcao == 'direita':
            self.rect.x += self.velocidade

    def disparar(self):
        """Retorna um projétil disparado pela nave."""
        largura_projetil = 5
        altura_projetil = 10
        cor_projetil = (255, 0, 0)  # Vermelho
        velocidade_projetil = -10  # Sobe na tela
        
        return Laser(
            self.rect.centerx - largura_projetil // 2,
            self.rect.top - altura_projetil,
            largura_projetil,
            altura_projetil,
            cor_projetil,
            velocidade_projetil
        )
