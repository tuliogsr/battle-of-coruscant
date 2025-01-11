import pygame
import Interface.jogo_space as jogo
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carrega a imagem do jogador
        self.image = pygame.image.load("src/Assents/NavePrincipal.jpg")  # Ajuste a escala conforme necessário
        self.rect = self.image.get_rect()
        self.rect.centerx =  self.screen_width// 2
        self.rect.bottom = self.screen_height - 10
        self.speed = 5
        self.cooldown = 250
        self.last_shot = pygame.time.get_ticks()
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.y += self.velocity
