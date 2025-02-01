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
YELLOW = (255, 255, 0)
RED = (200, 0, 0)

# Load assets
bg = pygame.image.load("bg.jpg")  # Background image
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("loopy Bird")

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(100, 400)
    pipes.append([WIDTH, pipe_height, False])  # False means score hasn't been counted yet

# Countdown before the game starts
def countdown():
    for i in range(3, 0, -1):
        screen.blit(bg, (0, 0))
        text = FONT.render(f"Starting in {i}...", True, BLUE)
        screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(1)

# Start screen
def start_screen():
    screen.fill(WHITE)
    text = FONT.render("Press SPACE to start", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Game over screen
def game_over(final_score):
    screen.fill(WHITE)
    text1 = FONT.render("Game Over!", True, BLACK)
    score_text = FONT.render(f"Final Score: {final_score}", True, BLACK)
    text2 = FONT.render("Press R to Restart", True, BLACK)
    text3 = FONT.render("or", True, BLACK)
    text4 = FONT.render("Q to Quit", True, BLACK)

    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    text3_rect = text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    text4_rect = text4.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

    screen.blit(text1, text1_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(text2, text2_rect)
    screen.blit(text3, text3_rect)
    screen.blit(text4, text4_rect)

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game()  # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def draw_bird(y):
    """Draw a simple bird with a circle body, eye, and beak"""
    pygame.draw.ellipse(screen, BLUE, (BIRD_X - 20, BIRD_Y - 10, 20, 10), 3)
    pygame.draw.ellipse(screen, BLUE, (BIRD_X, BIRD_Y - 10, 20, 10), 3)

def draw_pipes():
    """Draw pipes with rounded edges for a smoother look"""
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe[0], 0, PIPE_WIDTH, pipe[1]), border_radius=10)
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe[1] - PIPE_GAP), border_radius=10)

def main_game():
    global BIRD_Y, bird_y_velocity, pipes, scores, PIPE_SPEED
    BIRD_Y = HEIGHT // 2
    bird_y_velocity = 0
    pipes = []
    scores = 0
    PIPE_SPEED = 5  # Start with the base speed
    running = True
    bg_x = 0  # Background scrolling position
    
    start_screen()
    countdown()
    create_pipe()

    clock = pygame.time.Clock()
    while running:
        # Scroll background
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + WIDTH, 0))
        bg_x -= 2
        if bg_x <= -WIDTH:
            bg_x = 0  # Reset background position
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_velocity = JUMP_STRENGTH
        
        # Bird physics
        bird_y_velocity += GRAVITY
        BIRD_Y += bird_y_velocity

        # Draw pipes
        draw_pipes()

        # Pipe movement and collision
        for pipe in pipes:
            pipe[0] -= PIPE_SPEED  # Move pipe left
            
            # Collision detection
            if (BIRD_X + BIRD_RADIUS > pipe[0] and BIRD_X - BIRD_RADIUS < pipe[0] + PIPE_WIDTH and
                (BIRD_Y - BIRD_RADIUS < pipe[1] or BIRD_Y + BIRD_RADIUS > pipe[1] + PIPE_GAP)):
                running = False
            
            # Score update
            if pipe[0] + PIPE_WIDTH < BIRD_X and not pipe[2]:  # Passed pipe
                scores += 1
                pipe[2] = True  # Mark pipe as counted
                
                # **Increase speed every 5 points**
                if scores % 5 == 0:
                    PIPE_SPEED += 1
        
        # Remove off-screen pipes and add new ones
        if pipes and pipes[0][0] < -PIPE_WIDTH:
            pipes.pop(0)
            create_pipe()

        # Draw bird
        draw_bird(BIRD_Y)

        # Display score
        score_text = FONT.render(f"Score: {scores}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Check for game over
        if BIRD_Y > HEIGHT or BIRD_Y < 0:
            running = False
        
        pygame.display.flip()
        clock.tick(60)  # **Smoother 60 FPS**

    game_over(scores)  # Show game over screen with final score

# Run the game
main_game()
