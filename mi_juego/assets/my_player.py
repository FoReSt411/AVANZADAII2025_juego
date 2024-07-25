import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, '../images/player.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
