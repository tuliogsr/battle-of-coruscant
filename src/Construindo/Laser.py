import pygame

# Carregar imagens corretamente, certificando-se de incluir as extensões de arquivo
laser_inimigo = pygame.image.load("laser_inimigo.png")
laser_jogador = pygame.image.load("laser_jogador.png")

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mascarar = pygame.mask.from_surface(self.img)
    
    def mov_x_y(self, window):
        # Corrigir o uso do método blit
        window.blit(self.img, (self.x, self.y))

    def mover(self, vel):
        self.y += vel

    def sair_tela(self, altura):
        # Corrigir o operador de comparação
        return not(0 <= self.y <= altura)

    def colisao(self, objeto):
        # Usar pygame.Rect.colliderect para verificar colisão
        objeto_rect = pygame.Rect(objeto.x, objeto.y, objeto.img.get_width(), objeto.img.get_height())
        self_rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        return self_rect.colliderect(objeto_rect)
