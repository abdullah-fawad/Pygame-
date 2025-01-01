import pygame
import random
import sys


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 50  
JUMP_HEIGHT = 190  
JUMP_VELOCITY = -18  
GRAVITY = 1.2 
BLOCK_SPEED = 8 
GAP_WIDTH = 150  
ROAD_Y = SCREEN_HEIGHT - 100 


LIGHT_BROWN = (222, 184, 135)
DARK_BLUE = (0, 0, 139)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump Over the Gaps")
font = pygame.font.SysFont(None, 36)


# Player class (block)
class Player:
    def __init__(self):
        self.x = 100
        self.y = ROAD_Y - BLOCK_SIZE
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.vel_y = 0  
        self.is_jumping = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.vel_y = JUMP_VELOCITY  
            self.is_jumping = True

        # Apply gravity
        if self.is_jumping:
            self.y += self.vel_y
            self.vel_y += GRAVITY  

            # If the player reaches the ground, stop jumping
            if self.y >= ROAD_Y - BLOCK_SIZE:
                self.y = ROAD_Y - BLOCK_SIZE
                self.is_jumping = False

    def draw(self):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))

# Gap class 
class Gap:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = ROAD_Y
        self.width = GAP_WIDTH

    def move(self):
        self.x -= BLOCK_SPEED  # Move gap to the left

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, BLOCK_SIZE)) 

    def off_screen(self):
        return self.x + self.width < 0

# Main game loop
def game_loop():
    player = Player()
    gaps = [Gap()]
    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(LIGHT_BROWN)  

        pygame.draw.rect(screen, DARK_BLUE, (0, ROAD_Y, SCREEN_WIDTH, BLOCK_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        player.move()
        player.draw()

       
        for gap in gaps:
            gap.move()
            gap.draw()

            # Check for collisions with gaps (if the player is not jumping and is on the ground)
            if (player.x + player.width > gap.x and player.x < gap.x + gap.width and
                player.y + player.height == ROAD_Y):
                # If the player lands in the gap, the game ends
                game_over(score)

            # Remove gaps that have gone off-screen and add new ones
            if gap.off_screen():
                gaps.remove(gap)
                gaps.append(Gap())  # Add a new gap at the right edge
                score += 1  # Increase score when a gap is passed

        # Display the score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# Game Over screen
def game_over(score):
    screen.fill(LIGHT_BROWN)
    game_over_text = font.render("GAME OVER!", True, BROWN)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Wait for the player to press any key to restart
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Restart the game if space is pressed
                    game_loop()

# Start the game loop
if __name__ == "__main__":
    game_loop()
