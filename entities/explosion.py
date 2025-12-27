import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.explosion_images = []
        
        
        for i in range(1, 6):
            img = pygame.image.load(f"assets/images/exp{i}.png")
            self.explosion_images.append(img)
        
        self.index = 0
        self.image = self.explosion_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.animation_speed = 4  

    def update(self):
        self.counter += 1
        
        if self.counter >= self.animation_speed and self.index < len(self.explosion_images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.explosion_images[self.index]
        
        if self.index >= len(self.explosion_images) - 1 and self.counter >= self.animation_speed:
            self.kill()
