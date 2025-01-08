import pygame

laser_inimigo = pygame.image.load("laser_inimigo")
laser_jogador = pygame.image.load("laser_jogador")

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mascarar = pygame.mask.from_surface(self.img)
    
    def mov_x_y(self, window): #Laser se movimento nos eixos x e y
        window.blit(self.img(self.x, self.y))

    def mover(self, vel):
        self.y += vel

    def sair_tela(self, altura): #Se laser sair da tela, nada acontece, ele apenas é removido
        return not(self.y <= altura and self.y=0)

    def colisao(self, objeto):
        return pygame.Rect.collide(self, objeto)