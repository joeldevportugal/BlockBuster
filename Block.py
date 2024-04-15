import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição de constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLOCK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlockBuster")


# Definição da plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Definição da bola
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 5
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

# Definição do bloco
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((80, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Inicialização dos sprites
all_sprites = pygame.sprite.Group()
platform = Platform()
ball = Ball()
all_sprites.add(platform, ball)

# Criação dos blocos
blocks = pygame.sprite.Group()
for row in range(5):
    for col in range(10):
        color = random.choice(BLOCK_COLORS)
        block = Block(85 * col + 35, 30 * row + 20, color)
        blocks.add(block)
        all_sprites.add(block)

# Definição das vidas
font = pygame.font.Font(None, 36)
lives = 5

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                platform.speed = -5
            elif event.key == pygame.K_RIGHT:
                platform.speed = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                platform.speed = 0

    # Atualização dos sprites
    all_sprites.update()

    # Verificação de colisões
    if pygame.sprite.collide_rect(ball, platform):
        ball.speed_y *= -1

    # Verificação de colisões entre a bola e os blocos
    block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
    if len(block_hit_list) > 0:
        ball.speed_y *= -1

    # Verificação de perda de vida
    if ball.rect.top >= SCREEN_HEIGHT:
        lives -= 1
        if lives <= 0:
            running = False
        else:
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_y *= -1

    # Desenho na tela
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Exibição das vidas
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()

    # Limitação de quadros por segundo
    clock.tick(60)

# Encerramento do Pygame
pygame.quit()
sys.exit()
