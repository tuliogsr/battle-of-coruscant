import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("path_to_player_image.png")
        self.x = x
        self.y = y
        self.velocity = 5
    
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
