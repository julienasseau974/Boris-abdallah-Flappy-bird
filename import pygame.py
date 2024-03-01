import pygame
import random

# Initialiser Pygame
pygame.init()

# Constantes du jeu
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
GRAVITY = 0.25
BIRD_MOVEMENT = 0
GAME_ACTIVE = True

# Couleurs
BLUE_SKY = (113, 197, 207)

# Configuration de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Horloge
clock = pygame.time.Clock()

# Charger les images
bird_surface = pygame.image.load("bird.png").convert_alpha()  # Assurez-vous que bird.png est dans le même dossier que ce script
bird_surface = pygame.transform.scale(bird_surface, (50, 35))  # Optionnel : redimensionner l'image si nécessaire
ground_surface = pygame.Surface((SCREEN_WIDTH, 100))
ground_surface.fill((222, 184, 135))
background_surface = pygame.image.load("background.png").convert()  # Charger l'image de fond
background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionner l'image de fond si nécessaire
pipe_surface = pygame.image.load("pipe.png").convert_alpha()  # Assurez-vous que l'image est dans le bon dossier
pipe_surface = pygame.transform.scale(pipe_surface, (80, 500))  # Ajustez ces valeurs selon la taille souhaitée



# Position et rect de l'oiseau
bird_rect = bird_surface.get_rect(center=(100, SCREEN_HEIGHT // 2))

# Sol
ground_y = SCREEN_HEIGHT - 100

# Obstacles
pipe_surface = pygame.Surface((80, 500))
pipe_surface.fill((0, 128, 0))  # Vert pour les tuyaux
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= ground_y:
        return False
    return True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                BIRD_MOVEMENT = 0
                BIRD_MOVEMENT -= 6
            if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                GAME_ACTIVE = True
                pipe_list.clear()
                bird_rect.center = (100, SCREEN_HEIGHT // 2)
                BIRD_MOVEMENT = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
    screen.blit(background_surface, (0, 0))
 


    if GAME_ACTIVE:
        # Oiseau
        BIRD_MOVEMENT += GRAVITY
        bird_rect.centery += BIRD_MOVEMENT
        screen.blit(bird_surface, bird_rect)
        GAME_ACTIVE = check_collision(pipe_list)

        # Tuyaux
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Sol
    screen.blit(ground_surface, (0, ground_y))

    pygame.display.update()
    clock.tick(120)  # Maintient le jeu à 120 FPS