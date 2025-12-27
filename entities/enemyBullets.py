import pygame

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.kill()
			