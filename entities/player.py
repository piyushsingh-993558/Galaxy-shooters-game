import pygame
from .bullet import Bullets

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 5
        self.screen_width = screen_width
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 300  # milliseconds between shots
        
    def update(self):
        # Get key presses
        keys = pygame.key.get_pressed()
        
        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            
        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # Play shooting sound effect
            return Bullets(self.rect.centerx, self.rect.top)
        return None
