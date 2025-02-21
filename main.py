import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_X = 80
BIRD_RADIUS = 15
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 5
FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BLUE = (0, 162, 232)
BLACK = (0, 0, 0)

# Load assets
bg = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
land = pygame.transform.scale(pygame.image.load("land.png"), (WIDTH, 100)) 
cloud = pygame.transform.scale(pygame.image.load("cloud.webp"), (80, 50))
tree = pygame.transform.scale(pygame.image.load("tree.webp"), (60, 100))

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loopy Bird")

def create_pipe():
    """Creates a new pipe with a random height."""
    pipe_height = random.randint(100, 400)
    return [WIDTH, pipe_height, False]

def countdown():
    """Displays a countdown before the game starts."""
    for i in range(3, 0, -1):
        screen.blit(bg, (0, 0))
        text = FONT.render(f"Starting in {i}...", True, BLUE)
        screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(1)

def start_screen():
    """Displays the start screen and waits for SPACE key press."""
    screen.fill(WHITE)
    text = FONT.render("Press SPACE to start", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def game_over(final_score):
    """Displays the game over screen with the final score."""
    screen.fill(WHITE)
    texts = ["Game Over!", f"Final Score: {final_score}", "Press R to Restart", "or", "Q to Quit"]
    for i, t in enumerate(texts):
        text = FONT.render(t, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70 + (i * 30)))
        screen.blit(text, text_rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def draw_bird(y):
    """Draws the bird."""
    pygame.draw.ellipse(screen, WHITE, (BIRD_X - 20, y - 10, 20, 10), 3)
    pygame.draw.ellipse(screen, WHITE, (BIRD_X, y - 10, 20, 10), 3)

def draw_pipes(pipes):
    """Draws all pipes."""
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe[0], 0, PIPE_WIDTH, pipe[1]), border_radius=10)
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe[1] - PIPE_GAP), border_radius=10)

def main_game():
    """Main game loop."""
    bird_y = HEIGHT // 2
    bird_y_velocity = 0
    pipes = [create_pipe()]
    score = 0
    pipe_speed = PIPE_SPEED
    bg_x = 0
    running = True
    
    start_screen()
    countdown()
    clock = pygame.time.Clock()
    
    while running:
        screen.blit(bg, (bg_x, 0))  # Draw background
        screen.blit(bg, (bg_x + WIDTH, 0))  # For scrolling effect
        screen.blit(land, (0, HEIGHT - 100))  # Draw land at the bottom
        screen.blit(cloud, (WIDTH // 2, 100))
        screen.blit(tree, (30, HEIGHT - 120))
        screen.blit(tree, (WIDTH - 90, HEIGHT - 120))
        
        bg_x = (bg_x - 2) % -WIDTH  # Scrolling background effect
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_y_velocity = JUMP_STRENGTH
        
        bird_y_velocity += GRAVITY
        bird_y += bird_y_velocity
        
        for pipe in pipes:
            pipe[0] -= pipe_speed
            if (BIRD_X + BIRD_RADIUS > pipe[0] and BIRD_X - BIRD_RADIUS < pipe[0] + PIPE_WIDTH and
                (bird_y - BIRD_RADIUS < pipe[1] or bird_y + BIRD_RADIUS > pipe[1] + PIPE_GAP)):
                running = False
            if pipe[0] + PIPE_WIDTH < BIRD_X and not pipe[2]:
                score += 1
                pipe[2] = True
                if score % 5 == 0:
                    pipe_speed += 1
        
        if pipes and pipes[0][0] < -PIPE_WIDTH:
            pipes.pop(0)
            pipes.append(create_pipe())
        
        draw_pipes(pipes)
        draw_bird(bird_y)
        score_text = FONT.render(f"Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, WHITE, score_rect.inflate(10, 10))  # White box with padding
        screen.blit(score_text, score_rect)

        if bird_y > HEIGHT or bird_y < 0:
            running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    game_over(score)

main_game()
