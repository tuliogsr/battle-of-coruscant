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

'''

import pygame
import sys

from include.laser import Laser

class Nave():
    cooldown = 30
    def _init_(self, x, y, saude=100):
        self.x = x
        self.y = y
        self.saude = saude
        self.nave_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_cont = 0

    def draw(self, window):
        window.blit(self.nave_img,(self.x,self.y))
        for laser in self.lasers: #fogo amigo permitido para inimigos
            laser.draw(window)

    def movimento_laser(self, vel, objeto): 
        self.cooldown()
        for laser in self.lasers:
            laser.mover(vel)
            if laser.sair_tela(height):
                self.lasers.remove(laser) #laser sai da tela ao não acertar ninguem
            elif laser.colisao(objeto):
                objeto.saude -= 10 #a cada dano sofrido, jogador leva 10 de dano
                self.lasers.remove(laser) #laser sai da tela ao colidir
    
    def espera_tiro(self): #cooldown de tiro
        if self.cooldown_cont >= self.cooldown:
            self.cooldown_cont = 0
        elif self.cooldown_cont > 0:
            self.cooldown_cont += 1

    def tiro(self): #funcionamento do tiro
        if self.cooldown_cont == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_cont = 1

    def get_largura(self):
        return self.nave_img.get_largura()

    def get_altura(self):
        return self.nave_img.get_altura()

'''