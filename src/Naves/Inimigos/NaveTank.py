import pygame
from src.Naves.NaveBase.Naves import Nave
from src.Naves.NaveBase.Laser import Laser

class NaveTank(Nave):
    def __init__(self, x, y, largura, altura, cor, velocidade, vida):
        """
        Inicializa uma nave tank.
        
        Args:
            x (int): Posição inicial no eixo X.
            y (int): Posição inicial no eixo Y.
            largura (int): Largura da nave.
            altura (int): Altura da nave.
            cor (tuple): Cor da nave (R, G, B).
            velocidade (int): Velocidade de movimentação da nave.
            vida (int): Vida inicial da nave.
        """
        super().__init__(x, y, largura, altura, cor, velocidade)
        self.vida = vida

    def receber_dano(self, dano):
        """Reduz a vida da nave tank."""
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0  # Evita valores negativos

    def disparar(self):
        """
        Sobrescreve o método de disparo para criar projéteis maiores ou mais poderosos.
        
        Returns:
            Projeteis: O projétil disparado pela nave tank.
        """
        largura_projetil = 10  # Projétil maior
        altura_projetil = 15
        cor_projetil = (255, 255, 0)  # Amarelo
        velocidade_projetil = -8  # Velocidade menor, mas dano maior
        
        return Laser(
            self.rect.centerx - largura_projetil // 2,
            self.rect.top - altura_projetil,
            largura_projetil,
            altura_projetil,
            cor_projetil,
            velocidade_projetil
        )
