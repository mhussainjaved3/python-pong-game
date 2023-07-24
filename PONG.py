import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
BALL_SPEED = 5
PADDLE_SPEED = 5
WHITE = (255, 255, 255)
FPS = 60

# Refactoring: Create a function to handle paddle movement
def move_paddle(paddle, direction):
    if direction == "UP":
        paddle.y -= PADDLE_SPEED
    elif direction == "DOWN":
        paddle.y += PADDLE_SPEED

# Refactoring: Create a function to handle ball movement
def move_ball(ball, ball_speed):
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

# Exception Handling: Create a function to quit the game safely
def quit_game():
    pygame.quit()
    sys.exit()

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Create the paddles and ball
player_paddle = pygame.Rect(10, HEIGHT // 2 - 50, 10, 100)
opponent_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)

# Set the initial ball speed
ball_speed = [BALL_SPEED, BALL_SPEED]

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_paddle(player_paddle, "UP")
    if keys[pygame.K_s]:
        move_paddle(player_paddle, "DOWN")

    # Opponent AI controls (simple AI that follows the ball)
    if ball.centery < opponent_paddle.centery:
        move_paddle(opponent_paddle, "UP")
    elif ball.centery > opponent_paddle.centery:
        move_paddle(opponent_paddle, "DOWN")

    # Move the ball
    move_ball(ball, ball_speed)

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed[0] = -ball_speed[0]

    # Ball out of bounds (score points)
    if ball.left <= 0:
        # Exception Handling: Catch an exception if there is an error writing to the file
        try:
            with open("scores.txt", "a") as file:
                file.write("Player 2 scores!\n")
        except IOError:
            print("An error occurred while writing to the file.")

        ball_speed = [BALL_SPEED, BALL_SPEED]
        ball.x = WIDTH // 2 - 10
        ball.y = HEIGHT // 2 - 10

    if ball.right >= WIDTH:
        try:
            with open("scores.txt", "a") as file:
                file.write("Player 1 scores!\n")
        except IOError:
            print("An error occurred while writing to the file.")

        ball_speed = [-BALL_SPEED, -BALL_SPEED]
        ball.x = WIDTH // 2 - 10
        ball.y = HEIGHT // 2 - 10

    # Draw everything on the screen
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)
