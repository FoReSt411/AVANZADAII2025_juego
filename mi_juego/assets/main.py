import pygame
import settings
from my_player import Player

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))  # Corrección: set_mode
pygame.display.set_caption(settings.TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(settings.FPS)

pygame.quit()
