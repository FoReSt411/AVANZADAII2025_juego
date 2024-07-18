
import settigns
import pygame

pygame.init()
screen = pygame.display.set_smode((settigns.WHIDTH, settigns.HEIGHT))
pygame.display.set_caption(settigns.TITLE)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(settigns.FPS)

pygame.quit()