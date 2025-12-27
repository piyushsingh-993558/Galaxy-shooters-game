# import pygame

# class BaseEntity(pygame.sprite.Sprite):
#     """Base class for all game entities"""
    
#     def __init__(self, x, y, image_path):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(image_path)
#         self.rect = self.image.get_rect()
#         self.rect.center = [x, y]
        
#     def update(self):
#         """Update method to be overridden by subclasses"""
#         pass
        
#     def get_position(self):
#         """Return current position"""
#         return self.rect.center
        
#     def set_position(self, x, y):
#         """Set position"""
#         self.rect.center = [x, y]