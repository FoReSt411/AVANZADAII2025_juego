import pygame
import settings
import os
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption(settings.TITLE)
clock = pygame.time.Clock()

# Cargar imágenes
current_dir = os.path.dirname(__file__)
player_image = pygame.image.load(os.path.join(current_dir, '../images/player.png')).convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 60))
player2_image = pygame.image.load(os.path.join(current_dir, '../images/player2.png')).convert_alpha()
player2_image = pygame.transform.scale(player2_image, (50, 60))
background_image = pygame.image.load(os.path.join(current_dir, '../images/background.png')).convert_alpha()

# Cargar y redimensionar el logo
logo_image = pygame.image.load(os.path.join(current_dir, '../images/logo.png')).convert_alpha()
logo_size = (280, 200)  # Tamaño deseado para el logo
logo_image = pygame.transform.scale(logo_image, logo_size)  # Redimensionar el logo

# Función para cargar y obtener los frames del GIF
def load_gif_frames(gif_path, size):
    pil_image = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = pil_image.resize(size, Image.Resampling.LANCZOS)  # Redimensionar el frame
            frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert_alpha()
            frames.append(frame)
            pil_image.seek(pil_image.tell() + 1)
    except EOFError:
        pass
    return frames

# Cargar frames del GIF para el menú y redimensionar a 1000x500
gif_path = os.path.join(current_dir, '../images/menu_background2.gif')
menu_background_frames = load_gif_frames(gif_path, (settings.WIDTH, settings.HEIGHT))

# Función del menú principal
def main_menu():
    menu_running = True
    intro_index = 0
    frame_delay = 100  # Tiempo en milisegundos entre frames
    last_frame_time = pygame.time.get_ticks()

    # Definir fuente para el menú
    font_size = 48  # Tamaño mayor para el texto
    font = pygame.font.Font(None, font_size)
    text_color = (0, 0, 0)  # Negro

    while menu_running:
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time > frame_delay:
            intro_index = (intro_index + 1) % len(menu_background_frames)
            last_frame_time = current_time

        # Mostrar el frame del GIF
        screen.blit(menu_background_frames[intro_index], (0, 0))

        # Mostrar el logo sobre la imagen de fondo
        logo_rect = logo_image.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 200))  # Mover el logo 200 píxeles hacia arriba
        screen.blit(logo_image, logo_rect)

        # Mostrar el texto "PRESIONA ENTER PARA INICIAR" y "PRESIONA ESC PARA SALIR"
        play_text = font.render("Press ENTER to Play", True, text_color)
        exit_text = font.render("Press ESC to Exit", True, text_color)
        screen.blit(play_text, (settings.WIDTH // 2 - play_text.get_width() // 2, settings.HEIGHT // 2))
        screen.blit(exit_text, (settings.WIDTH // 2 - exit_text.get_width() // 2, settings.HEIGHT // 2 + font_size + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Clase para la selección de personajes
class CharacterSelection:
    def __init__(self):
        self.character_images = [
            pygame.image.load(os.path.join(current_dir, '../characters/character1.png')).convert_alpha(),
            pygame.image.load(os.path.join(current_dir, '../characters/character2.png')).convert_alpha(),
            pygame.image.load(os.path.join(current_dir, '../characters/character3.png')).convert_alpha(),
            pygame.image.load(os.path.join(current_dir, '../characters/character4.png')).convert_alpha()
        ]
        self.character_size = (100, 100)
        self.character_images = [pygame.transform.scale(img, self.character_size) for img in self.character_images]
        self.player1_selection = 0
        self.player2_selection = 1
        self.selected_rect_color = (0, 0, 255)  # Color azul para el marco de selección
        self.border_thickness = 5
        self.font = pygame.font.Font(None, 36)
        self.player1_confirmed = False
        self.player2_confirmed = False

    def draw(self):
        screen.blit(background_image, (0, 0))

        for i, img in enumerate(self.character_images):
            x = 100 + i * 120
            y = 200
            screen.blit(img, (x, y))
            if i == self.player1_selection:
                pygame.draw.rect(screen, self.selected_rect_color, (x, y, self.character_size[0], self.character_size[1]), self.border_thickness)
            if i == self.player2_selection:
                pygame.draw.rect(screen, self.selected_rect_color, (x, y + 150, self.character_size[0], self.character_size[1]), self.border_thickness)

        instruction_text = self.font.render("Player 1: WASD to select, SPACE to confirm", True, (255, 255, 255))
        screen.blit(instruction_text, (50, 50))
        instruction_text = self.font.render("Player 2: Arrow keys to select, ENTER to confirm", True, (255, 255, 255))
        screen.blit(instruction_text, (50, 100))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if not self.player1_confirmed:
                    if event.key == pygame.K_w:
                        self.player1_selection = (self.player1_selection - 1) % len(self.character_images)
                    if event.key == pygame.K_s:
                        self.player1_selection = (self.player1_selection + 1) % len(self.character_images)
                    if event.key == pygame.K_SPACE:
                        self.player1_confirmed = True
                        print(f"Player 1 selected character {self.player1_selection + 1}")

                if not self.player2_confirmed:
                    if event.key == pygame.K_UP:
                        self.player2_selection = (self.player2_selection - 1) % len(self.character_images)
                    if event.key == pygame.K_DOWN:
                        self.player2_selection = (self.player2_selection + 1) % len(self.character_images)
                    if event.key == pygame.K_RETURN:
                        self.player2_confirmed = True
                        print(f"Player 2 selected character {self.player2_selection + 1}")

    def run(self):
        while not (self.player1_confirmed and self.player2_confirmed):
            self.handle_events()
            self.draw()
            clock.tick(60)

        return self.player1_selection, self.player2_selection

# Función para el menú de opciones de juego
def game_options_menu():
    menu_running = True
    font_size = 36
    font = pygame.font.Font(None, font_size)
    text_color = (0, 0, 0)
    highlight_color = (0, 0, 255)  # Azul para resaltar
    options = [
        "Battle Player vs Player",
        "Survival Mode",
        "Free Mode",
        "Solo vs AI",
        "ESC to Exit"
    ]
    selected_option = 0

    while menu_running:
        screen.fill((255, 255, 255))  # Fondo blanco

        # Mostrar el texto de opciones de juego
        for i, option in enumerate(options):
            text = font.render(option, True, text_color)
            rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 100 + i * (font_size + 10)))
            screen.blit(text, rect)

            # Resaltar la opción seleccionada
            if i == selected_option:
                pygame.draw.rect(screen, highlight_color, rect.inflate(20, 10), 2)  # Dibuja un marco azul alrededor del texto

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == len(options) - 1:
                        pygame.quit()
                        exit()
                    else:
                        if selected_option == 0:
                            player1_char, player2_char = CharacterSelection().run()
                            print(f"Player 1 selected character: {player1_char + 1}")
                            print(f"Player 2 selected character: {player2_char + 1}")
                        elif selected_option == 1:
                            print("Survival Mode selected")
                        elif selected_option == 2:
                            print("Free Mode selected")
                        elif selected_option == 3:
                            print("Solo vs AI selected")
                        menu_running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Clase Player (debe estar definida en tu código original)
class Player(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, controls):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 5
        self.controls = controls  # (arriba, izquierda, abajo, derecha)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls[1]]:  # Movimiento izquierda
            self.rect.x -= self.speed
        if keys[self.controls[3]]:  # Movimiento derecha
            self.rect.x += self.speed
        if keys[self.controls[0]]:  # Movimiento arriba
            self.rect.y -= self.speed
        if keys[self.controls[2]]:  # Movimiento abajo
            self.rect.y += self.speed

# Función principal del juego
def game():
    all_sprites = pygame.sprite.Group()

    player1 = Player(player_image, (200, 100), (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d))  # Jugador 1
    player2 = Player(player2_image, (400, 300), (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT))  # Jugador 2

    all_sprites.add(player1, player2)

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

# Llamar al menú principal antes de iniciar el juego
main_menu()
game_options_menu()
game()
