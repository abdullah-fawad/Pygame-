import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game settings
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
#
# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
snake_direction = "RIGHT"
score = 0

# Food settings
def generate_food():
    max_x = (WINDOW_WIDTH // CELL_SIZE) - 1
    max_y = (WINDOW_HEIGHT // CELL_SIZE) - 1
    return (random.randint(0, max_x) * CELL_SIZE, random.randint(0, max_y) * CELL_SIZE)

food_position = generate_food()

# Font settings for score display
font = pygame.font.Font(None, 36)

# Function to draw the snake
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Function to draw the food
def draw_food():
    pygame.draw.ellipse(screen, RED, pygame.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))

# Function to move the snake
def move_snake():
    global food_position, score

    head_x, head_y = snake[0]
    if snake_direction == "UP":
        head_y -= CELL_SIZE
    elif snake_direction == "DOWN":
        head_y += CELL_SIZE
    elif snake_direction == "LEFT":
        head_x -= CELL_SIZE
    elif snake_direction == "RIGHT":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)
    snake.insert(0, new_head)

    # Check for collision with food
    if new_head == food_position:
        score += 1
        food_position = generate_food()
    else:
        snake.pop()

# Function to check for collisions with walls or self
def check_collisions():
    head_x, head_y = snake[0]

    # Check if snake hits the boundaries
    if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < 0 or head_y >= WINDOW_HEIGHT:
        return True

    # Check if snake collides with itself
    if snake[0] in snake[1:]:
        return True

    return False

# Function to display the score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to end the game
def end_game():
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! Your score: {score}", True, WHITE)
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Game loop
clock = pygame.time.Clock()
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # Move the snake
    move_snake()

    # Check for collisions
    if check_collisions():
        end_game()

    # Fill screen
    screen.fill(BLACK)

    # Draw everything
    draw_snake()
    draw_food()
    display_score()

    # Refresh game screen
    pygame.display.flip()

    # fps
    clock.tick(10)
