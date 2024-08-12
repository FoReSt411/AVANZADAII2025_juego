# my_player2.py
import pygame

class My_player2(pygame.sprite.Sprite):
    def __init__(self, images, start_pos, controls):
        super().__init__()
        self.images = images
        self.image = self.images[0]  # Primer frame
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 5
        self.controls = controls
        self.frame_index = 0
        self.frame_delay = 100
        self.last_frame_time = pygame.time.get_ticks()

        self.initial_y = start_pos[1]
        self.is_jumping = False
        self.jump_speed = -15
        self.gravity = 1
        self.velocity_y = 0
        self.jump_height = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls[1]]:
            self.rect.x -= self.speed
        if keys[self.controls[3]]:
            self.rect.x += self.speed

        if keys[self.controls[0]] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_speed

        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity

            if self.rect.y >= self.initial_y:
                self.rect.y = self.initial_y
                self.is_jumping = False
                self.velocity_y = 0

        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]
            self.last_frame_time = current_time
