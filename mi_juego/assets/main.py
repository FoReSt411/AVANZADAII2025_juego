
import pygame
import settings
import os
from PIL import Image

# Configuración inicial
pygame.init()

# Definir tamaño de la ventana y pantalla completa
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60
# Definir el título y el reloj
pygame.display.set_caption(settings.TITLE)
clock = pygame.time.Clock()

# Cargar imágenes
current_dir = os.path.dirname(__file__)
background_image_path = os.path.join(current_dir, '../images/background.png')
logo_image_path = os.path.join(current_dir, '../images/logo.png')

try:
    background_image = pygame.image.load(background_image_path).convert_alpha()
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))  # Fallback to a solid color

try:
    logo_image = pygame.image.load(logo_image_path).convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (280, 200))
except pygame.error as e:
    print(f"Error loading logo image: {e}")
    logo_image = pygame.Surface((280, 200))  # Fallback to a solid color

# Función para cargar y obtener los frames del GIF
def load_gif_frames(gif_path, size):
    frames = []
    try:
        # Cargar el GIF usando Pygame
        pil_image = Image.open(gif_path)
        for frame in range(pil_image.n_frames):
            pil_image.seek(frame)
            frame_img = pil_image.convert('RGBA')
            frame_img = pygame.image.fromstring(frame_img.tobytes(), frame_img.size, 'RGBA').convert_alpha()
            frame_img = pygame.transform.scale(frame_img, size)
            frames.append(frame_img)
    except Exception as e:
        print(f"Error loading GIF frames: {e}")
    return frames

# Cargar frames del GIF para el menú y redimensionar a 1920x1080
gif_path = os.path.join(current_dir, '../images/menu_background2.gif')
menu_background_frames = load_gif_frames(gif_path, (WINDOW_WIDTH, WINDOW_HEIGHT))

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
        logo_rect = logo_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 200))  # Mover el logo 200 píxeles hacia arriba
        screen.blit(logo_image, logo_rect)

        # Mostrar el texto "PRESIONA ENTER PARA INICIAR" y "PRESIONA ESC PARA SALIR"
        play_text = font.render("Press ENTER to Play", True, text_color)
        exit_text = font.render("Press ESC to Exit", True, text_color)
        screen.blit(play_text, (WINDOW_WIDTH // 2 - play_text.get_width() // 2, WINDOW_HEIGHT // 2))
        screen.blit(exit_text, (WINDOW_WIDTH // 2 - exit_text.get_width() // 2, WINDOW_HEIGHT // 2 + font_size + 10))

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
class CharacterManager:
    def __init__(self):
        self.characters = {
            "Goku": self.load_gif('../characters/goku.gif'),
            "Naruto": self.load_gif('../characters/naruto.gif'),
            "Inuyasha": self.load_gif('../characters/inuyasha.gif'),
            "Ichigo": self.load_gif('../characters/ichigo.gif')
        }

    def load_gif(self, path):
        gif_frames = load_gif_frames(os.path.join(current_dir, path), (100, 100))
        return gif_frames

    def get_character_image(self, name):
        return self.characters[name]

    def get_character_names(self):
        return list(self.characters.keys())

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
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100 + i * (font_size + 10)))
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
                            # Iniciar el juego con dos personajes
                            player1_char, player2_char = "Goku", "Naruto"  # O selecciona personajes según lo que hayas decidido
                            game(player1_char, player2_char)
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
    def __init__(self, images, start_pos, controls):
        super().__init__()
        self.images = images
        self.image = self.images[0]  # Asignar el primer frame
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 5
        self.controls = controls  # (arriba, izquierda, abajo, derecha)
        self.frame_index = 0
        self.frame_delay = 100  # Tiempo en milisegundos entre frames
        self.last_frame_time = pygame.time.get_ticks()

        # Almacena la posición inicial vertical
        self.initial_y = start_pos[1]

        # Variables de salto
        self.is_jumping = False
        self.jump_speed = -15
        self.gravity = 1
        self.velocity_y = 0
        self.jump_height = 100  # Altura máxima del salto

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls[1]]:  # Movimiento izquierda
            self.rect.x -= self.speed
        if keys[self.controls[3]]:  # Movimiento derecha
            self.rect.x += self.speed
        
        if keys[self.controls[0]] and not self.is_jumping:  # Salto
            self.is_jumping = True
            self.velocity_y = self.jump_speed

        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity

            # Limitar el salto y el retorno al suelo
            if self.rect.y >= self.initial_y:
                self.rect.y = self.initial_y
                self.is_jumping = False
                self.velocity_y = 0

        # Actualizar el frame del GIF
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]
            self.last_frame_time = current_time



# Función principal del juego
def game(player1_char, player2_char):
    all_sprites = pygame.sprite.Group()

    # Instanciar el CharacterManager para obtener imágenes de personajes
    character_manager = CharacterManager()
    player1_images = character_manager.get_character_image(player1_char)  # Obtener imágenes del personaje seleccionado
    player2_images = character_manager.get_character_image(player2_char)  # Obtener imágenes del personaje seleccionado

    # Crear los jugadores
    player1 = Player(player1_images, (200, WINDOW_HEIGHT - 250), (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d))
    player2 = Player(player2_images, (WINDOW_WIDTH - 350, WINDOW_HEIGHT - 250), (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT))

    all_sprites.add(player1, player2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # Detectar colisiones entre los jugadores usando máscaras
        if pygame.sprite.collide_mask(player1, player2):
            # Reaccionar a la colisión
            # Por ejemplo, detener el movimiento o realizar una acción
            player1.rect.x -= player1.speed  # Ajustar según sea necesario
            player2.rect.x += player2.speed  # Ajustar según sea necesario

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Llamar al menú principal antes de iniciar el juego
main_menu()
game_options_menu()