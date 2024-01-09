import pygame
import sys
import random

# Constants
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 15
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)

pygame.init()

# Set up the game window
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 40)

# Directions
# Each constant is a tuple representing the change in x and y coordinates corresponding to that direction
UP = (0, -SPACE_SIZE)           # No change in x-coordinate and decreasing y-coordinate by each SPACE_SIZE
DOWN = (0, SPACE_SIZE)          # No change in x-coordinate and increasing y-coordinate by each SPACE_SIZE
LEFT = (-SPACE_SIZE, 0)         # No change in y-coordinate and decreasing x-coordinate by each SPACE_SIZE
RIGHT = (SPACE_SIZE, 0)         # No change in y-coordinate and increasing x-coordinate by each SPACE_SIZE

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(window, SNAKE_COLOR, (segment[0], segment[1], SPACE_SIZE, SPACE_SIZE))

def draw_food(food):
    pygame.draw.ellipse(window, FOOD_COLOR, (food[0], food[1], SPACE_SIZE, SPACE_SIZE))

# Function to check collision with the walls or itself
def check_collision(snake):
    head = snake[0]
    if (
        head[0] < 0 or head[0] >= GAME_WIDTH or
        head[1] < 0 or head[1] >= GAME_HEIGHT
    ):
        return True
    
    # BUG: logic of collison of the snake with its own body. Need help here.
    for body_part in snake[1:]:
        if head == body_part[0] and head == body_part[1]:
            return True

    return False

# Initialize the snake and food
snake = [(i * SPACE_SIZE, 0) for i in range(BODY_PARTS)]
food = (random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE,
        random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE)
direction = RIGHT
score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != DOWN:
                direction = UP
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != UP:
                direction = DOWN
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != RIGHT:
                direction = LEFT
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != LEFT:
                direction = RIGHT

    # Move the snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check for collisions
    if check_collision(snake):
        # Handle game over
        window.fill(BACKGROUND_COLOR)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        window.blit(game_over_text, (GAME_WIDTH // 2 - 120, GAME_HEIGHT // 2 - 50))
        pygame.display.flip()
        continue

    # Check if the snake ate the food
    if snake[0] == food:
        food = (random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE,
                random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE)
        # snake.append(snake[-1])
        score += 1
    else:
        snake.pop()

    window.fill(BACKGROUND_COLOR)
    draw_snake(snake)
    draw_food(food)
    pygame.display.flip()

    # Display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    pygame.display.flip()

    clock.tick(SPEED)