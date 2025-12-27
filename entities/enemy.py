import pygame
import random
from .enemyBullets import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"assets/images/alien{random.randint(1, 5)}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1
        self.speed = 1
        self.screen_width = screen_width
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 3000) 
        self.shoot_chance = 0.002  

    def update(self):
        
        self.rect.x += self.move_direction * self.speed
        self.move_counter += 1
        
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
            self.rect.y += 20 
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.move_direction = 1
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.move_direction = -1

    def shoot(self):
        """Randomly shoot bullets to keep the game easy to play"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and random.random() < self.shoot_chance:
            self.last_shot = now
            self.shoot_delay = random.randint(1000, 3000)
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None