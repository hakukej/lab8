import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen and clock
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Constants for the game
SNAKE_SIZE = 10
FOOD_SIZE = 10
WIDTH, HEIGHT = 640, 480
LEVEL_UP_SCORE = 4

# Initialize variables
snake = [(100, 100), (90, 100), (80, 100)]  # Snake's body (list of segments)
direction = (SNAKE_SIZE, 0)  # Initial direction (moving right)
score = 0
level = 1
food_position = None
game_over = False
FPS = 15  # Initial FPS (game speed)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Function to draw the snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

# Function to generate a random food position that does not collide with the snake or walls
def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
        y = random.randint(0, (HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
        food_position = (x, y)
        if food_position not in snake:
            return food_position

# Function to display the score and level
def display_score_and_level(score, level):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game function
def main():
    global snake, direction, score, level, food_position, game_over, FPS

    # Generate the initial food position
    food_position = generate_food(snake)

    # Game loop
    while not game_over:
        screen.fill(BLACK)

        # Handle events (e.g., key presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, SNAKE_SIZE):
                    direction = (0, -SNAKE_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -SNAKE_SIZE):
                    direction = (0, SNAKE_SIZE)
                elif event.key == pygame.K_LEFT and direction != (SNAKE_SIZE, 0):
                    direction = (-SNAKE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-SNAKE_SIZE, 0):
                    direction = (SNAKE_SIZE, 0)

        # Move the snake by adding a new head in the direction and removing the tail
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake = [new_head] + snake[:-1]

        # Check for collisions with walls
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over = True

        # Check for collisions with the snake's own body
        if new_head in snake[1:]:
            game_over = True

        # Check if the snake eats food
        if new_head == food_position:
            snake.append(snake[-1])  # Add a new segment to the snake
            score += 1  # Increase the score
            food_position = generate_food(snake)  # Generate new food

            # Increase the level if score reaches threshold
            if score % LEVEL_UP_SCORE == 0:
                level += 1
                FPS += 2  # Increase the speed (FPS) with each level

        # Draw the snake and food
        draw_snake(snake)
        pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], FOOD_SIZE, FOOD_SIZE))

        # Display score and level
        display_score_and_level(score, level)

        # Update the screen
        pygame.display.flip()

        # Control the game speed (frames per second)
        clock.tick(FPS)

    # Game over
    pygame.quit()

# Run the game
main()
