import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()  # Initialize the font module

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 120, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
PADDLE_SPEED = 8
BALL_SPEED = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Fonts
font = pygame.font.Font(None, 36)

# Sounds
hit_sound = pygame.mixer.Sound("sounds/hitHurt1.wav")
game_over_sound = pygame.mixer.Sound("sounds/shoot_hit1.wav")
level_complete_sound = pygame.mixer.Sound("sounds/laserShoot1.wav")

# Create the paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [random.choice([-1, 1]) * BALL_SPEED, -BALL_SPEED]

# Create bricks
bricks = []
for row in range(5):
    for col in range(WIDTH // BRICK_WIDTH):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Game variables
score = 0
level = 1

# New Constants
GAME_OVER_TEXT = "Game Over"
RESTART_TEXT = "Press R to Restart"
PAUSE_TEXT = "Game Paused"
PAUSE_CONTINUE_TEXT = "Press P to Continue"

# New Variables
game_over = False
paused = False

def show_welcome_animation():
    text = "Welcome to Breakout Game"

    for i in range(len(text) + 1):
        screen.fill(BLACK)

        drawn_text = text[:i]
        text_surface = font.render(drawn_text, True, WHITE)
        x_position = WIDTH // 2 - text_surface.get_width() // 2
        y_position = HEIGHT // 2 - text_surface.get_height() // 2

        screen.blit(text_surface, (x_position, y_position))
        pygame.display.flip()
        pygame.time.Clock().tick(10)

    pygame.time.delay(1000)  # Pause for 1 second at the end of the animation

def show_intro_screen():
    intro_text = font.render("Let's start the Game", True, WHITE)
    screen.blit(intro_text, (WIDTH // 2 - intro_text.get_width() // 2, HEIGHT // 3 - intro_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the intro screen for 3 seconds

def show_final_score_animation():
    max_radius = max(WIDTH, HEIGHT)
    for radius in range(0, max_radius, 10):
        screen.fill(BLACK)
        score_text = font.render("Your Final Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), radius, 5)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def show_game_over_screen():
    global game_over, bricks, level, score

    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    level = 1
                    score = 0
                    bricks = []
                    for row in range(5 + level):
                        for col in range(WIDTH // BRICK_WIDTH):
                            brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
                            bricks.append(brick)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        game_over_text = font.render(GAME_OVER_TEXT, True, WHITE)
        restart_text = font.render(RESTART_TEXT, True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - game_over_text.get_height() // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # ... (previous code remains unchanged)


def show_pause_screen():
    global paused

    if paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        screen.fill(BLACK)
        pause_text = font.render(PAUSE_TEXT, True, WHITE)
        continue_text = font.render(PAUSE_CONTINUE_TEXT, True, WHITE)

        screen.blit(pause_text,
                    (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3 - pause_text.get_height() // 2))
        screen.blit(continue_text,
                    (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 - continue_text.get_height() // 2))

        pygame.display.flip()
        pygame.time.Clock().tick(30)


def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED


def handle_ball_movement():
    global score, level, bricks

    # Move the ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Collision with paddle
    if ball.colliderect(paddle) and ball_speed[1] > 0:
        ball_speed[1] = -ball_speed[1]
        hit_sound.play()

    # Collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]
            score += 10
            hit_sound.play()

    # Check if the ball is out of bounds (game over)
    if ball.bottom > HEIGHT:
        game_over_sound.play()
        show_final_score_animation()
        pygame.quit()
        sys.exit()

    # Check if the player completed the level
    if not bricks:
        level_complete_sound.play()
        level += 1
        bricks = []
        for row in range(5 + level):
            for col in range(WIDTH // BRICK_WIDTH):
                brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
                bricks.append(brick)


# ... (rest of the code remains unchanged)

# ... (previous code remains unchanged)

def draw_elements():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.circle(screen, RED, ball.center, BALL_RADIUS)

    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Display score and level
    score_text = font.render("Score: {}".format(score), True, WHITE)
    level_text = font.render("Level: {}".format(level), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

# ... (rest of the code remains unchanged)

def main():
    global bricks, level, score, game_over, paused  # Declare variables as global

    show_welcome_animation()
    show_intro_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    show_pause_screen()

        if not paused and not game_over:
            handle_input()
            handle_ball_movement()
            draw_elements()

            # Check if the player has won (reached a certain level)
            if level == 5:
                show_final_score_animation()
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Start the game
if __name__ == "__main__":
    main()
