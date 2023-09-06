import pygame
from pygame.locals import *
import sys
import jet
import flappybird
import snake

# Initialize Pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Initialize variables
game_options = ["Jet", "Snake", "Flappy Bird"]
selected_option = 0


# Function to start the selected game
def start_game():
    selected_game = game_options[selected_option]
    if selected_game == "Jet":
        jet.runJet()
    elif selected_game == "Snake":
        snake.runSnake()
    elif selected_game == "Flappy Bird":
        flappybird.runFlappyBird()


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                selected_option = (selected_option + 1) % len(game_options)
            elif event.key == K_UP:
                selected_option = (selected_option - 1) % len(game_options)
            elif event.key == K_RETURN:
                start_game()
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Clear the screen
    screen.fill((135, 206, 250))

    # Display the game options
    font = pygame.font.Font(None, 36)
    for i, option in enumerate(game_options):
        text_color = SELECTED_COLOR if i == selected_option else BLACK
        text = font.render(option, True, text_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 50))
        screen.blit(text, text_rect)

    # Draw the ">" symbol over the selected game text
    marker = font.render(">", True, SELECTED_COLOR)
    text_width = font.size(game_options[selected_option])[0]
    marker_rect = marker.get_rect(
        left=(SCREEN_WIDTH - text_width) // 2 - 30,
        centery=(200 + selected_option * 50)
    )
    screen.blit(marker, marker_rect)
    font = pygame.font.Font(None, 40)
    myname_surface = font.render("Ofek Yaloz", True, (0, 0, 0))
    myname_rect = myname_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(myname_surface, myname_rect)

    # Update the display
    pygame.display.flip()
