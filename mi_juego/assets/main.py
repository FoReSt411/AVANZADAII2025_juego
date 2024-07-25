import pygame
import settings
from my_player import Player
import os

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption(settings.TITLE)
clock = pygame.time.Clock()

# Cargar imágenes
current_dir = os.path.dirname(__file__)
player_image = pygame.image.load(os.path.join(current_dir, '../images/player.png')).convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 60))
background_image = pygame.image.load(os.path.join(current_dir, '../images/background.png')).convert_alpha()

# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 100)
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

# Crear grupo de sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
