import pygame

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This sets the name of the window
pygame.display.set_caption("Collision Example")

# Set the background color
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))


class Ball(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # set speed
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw_rect(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


if __name__ == "__main__":
    ball = Ball((255, 0, 0), 20, 15)
    ball.rect.x = 100
    ball.rect.y = 100

    obstacle1 = Obstacle((0, 0, 255), 100, 100, 300, 200)
    obstacle2 = Obstacle((0, 255, 0), 50, 50, 500, 300)

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(ball)
    all_sprites_list.add(obstacle1)
    all_sprites_list.add(obstacle2)

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.velocity_x = -3
                elif event.key == pygame.K_RIGHT:
                    ball.velocity_x = 3
                elif event.key == pygame.K_UP:
                    ball.velocity_y = -3
                elif event.key == pygame.K_DOWN:
                    ball.velocity_y = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ball.velocity_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ball.velocity_y = 0
        
        # Check for collisions with screen edges
        if ball.rect.x < 0 or ball.rect.x > screen_width - ball.rect.width:
            ball.velocity_x *=0
        if ball.rect.y < 0 or ball.rect.y > screen_height - ball.rect.height:
            ball.velocity_y *=0

        # Check for collision with obstacles
        if pygame.sprite.collide_rect(ball, obstacle1) or pygame.sprite.collide_rect(ball, obstacle2):
            ball.velocity_x *=0
            ball.velocity_y *=0

        ball.move()

        screen.fill((255, 255, 255))

        ball.draw_rect()
        screen.blit(obstacle1.image, obstacle1.rect)
        screen.blit(obstacle2.image, obstacle2.rect)

        all_sprites_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

  