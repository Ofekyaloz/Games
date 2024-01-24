import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
JUMP = 100
SPEED = 8
game_records = []
pygame.init()


def runDoodleJump():
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            original_image = pygame.image.load("images/doodle_jump_player.png").convert_alpha()
            scaled_size = (original_image.get_width() // 4, original_image.get_height() // 4)
            self.player_images = {
                0: pygame.transform.scale(original_image, scaled_size),
                1: pygame.transform.flip(pygame.transform.scale(original_image, scaled_size), True, False)
            }

            self.surf = self.player_images[0]

            self.rect = self.surf.get_rect(bottomleft=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.score = 0
            self.alive = True
            self.jumpHeight = 50
            self.jump = False
            self.on_obstacle = False  # New attribute to track if the player is on an obstacle

        def reset(self):
            self.rect = self.surf.get_rect(bottomleft=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
            self.score = 0
            self.alive = True
            self.surf = self.player_images[0]
            self.on_obstacle = False  # Reset the on_obstacle attribute

        def update(self, pressed_keys):

            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
                self.surf = self.player_images[0]

            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
                self.surf = self.player_images[1]

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

            if self.jump:
                if self.jumpHeight > 0:
                    self.rect.move_ip(0, -SPEED)
                    self.jumpHeight -= SPEED
                else:
                    self.jump = False
                    self.jumpHeight = JUMP
            else:
                self.rect.move_ip(0, SPEED)

            if not self.on_obstacle:  # Only check for collision when not already on an obstacle
                if self.rect.top <= 0:
                    self.rect.top = 0
                elif self.rect.bottom >= SCREEN_HEIGHT:
                    self.alive = False

        def player_jump(self):
            self.jumpHeight = JUMP
            self.jump = True

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, is_starting_obstacle=False):
            super(Obstacle, self).__init__()
            if is_starting_obstacle:
                self.surf = pygame.Surface((random.randint(100, 200), 10))
                self.rect = self.surf.get_rect(
                    center=(random.randint(20, SCREEN_WIDTH - 100), random.randint(10, SCREEN_HEIGHT)))
            else:
                self.surf = pygame.Surface((SCREEN_WIDTH, 10))
                self.rect = self.surf.get_rect(bottomleft=(0, SCREEN_HEIGHT - 8))
            self.surf.fill((0, 0, 0))

        def update(self):
            self.rect.move_ip(0, SPEED)  # Move the obstacle up
            if self.rect.bottom > SCREEN_HEIGHT:
                player.score += 1
                self.kill()

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("images/cloud.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # The starting position is randomly generated
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )

        # Move the cloud based on a constant speed
        # Remove it when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-4, 0)
            if self.rect.right < 0:
                self.kill()

    def render_score(score):
        score_str = str(score)
        digit_height = numbers[0].get_height()  # Assuming all digit images have the same height
        digit_width = numbers[0].get_width()  # Assuming all digit images have the same width

        # Calculate the total width and height for the score surface
        total_width = len(score_str) * (digit_width + 5)  # Adding 5 pixels of space between digits
        total_height = digit_height

        # Create a surface with alpha channel
        score_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)

        x_position = 0
        for digit_char in score_str:
            digit = int(digit_char)
            digit_image = numbers[digit]
            score_surface.blit(digit_image, (x_position, 0))
            x_position += digit_width + 3  # Add 5 pixels of space between digits

        return score_surface

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('DoodleJump by Ofek')

    ADDOBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDOBSTACLE, 1100)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1500)

    obstacles = pygame.sprite.Group()
    new_obstacle = Obstacle(False)
    obstacles.add(new_obstacle)

    clouds = pygame.sprite.Group()
    player = Player()

    run_game = True
    pause = False

    numbers = {}
    for i in range(10):
        numbers[i] = pygame.image.load("pic\\" + str(i) + ".png").convert()

    while run_game:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    run_game = False

                if event.key == K_p:
                    pause = not pause
                    if pause:
                        pygame.time.set_timer(ADDOBSTACLE, 0)  # Disable the obstacle event
                    else:
                        pygame.time.set_timer(ADDOBSTACLE, 1000)  # Enable the obstacle event with the desired interval

            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                run_game = False

            elif event.type == ADDOBSTACLE:
                # Create the new enemy, and add it to our sprite groups
                new_obstacle = Obstacle(True)
                obstacles.add(new_obstacle)

            elif event.type == ADDCLOUD:
                # Create the new cloud, and add it to our sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)

        if pause:
            # Display "Paused" message
            font = pygame.font.Font(None, 72)
            text = font.render("Paused", True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            clock.tick(30)
            continue

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        running = player.alive
        if player.rect.bottom < SCREEN_HEIGHT // 2:
            obstacles.update()
        clouds.update()

        screen.fill((135, 206, 250))

        for obstacle in obstacles:
            if player.rect.colliderect(obstacle) and player.rect.bottom >= obstacle.rect.top > player.rect.top:
                if not player.jump and player.rect.bottom <= obstacle.rect.bottom:
                    # Only jump if the player is not already jumping and is on top of the obstacle
                    player.player_jump()
                    player.on_obstacle = True
                else:
                    player.on_obstacle = False
            else:
                player.on_obstacle = False

        for cloud in clouds:
            screen.blit(cloud.surf, cloud.rect)

        for entity in obstacles:
            screen.blit(entity.surf, entity.rect)

        screen.blit(player.surf, player.rect)

        score_image = render_score(player.score)
        score_rect = score_image.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(score_image, score_rect)

        # Flip everything to the display
        pygame.display.flip()

        # Ensure we maintain a 30 frames per second rate
        clock.tick(30)

        if not running:
            game_records.append(player.score)
            game_records.sort(reverse=True)
            if len(game_records) > 5:
                game_records.pop()

            while not running:
                font = pygame.font.Font(None, 40)
                record_text = "Rank | Score"
                record_surface = font.render(record_text, True, (0, 0, 0))
                record_rect = record_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
                screen.blit(record_surface, record_rect)
                vertical_position = -170

                for i, score in enumerate(game_records):
                    i += 1
                    score_text = "{}. {}".format(i, score)
                    score_surface = font.render(score_text, True, (0, 0, 0))
                    score_rect = score_surface.get_rect(
                        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + vertical_position))
                    screen.blit(score_surface, score_rect)
                    vertical_position += 30

                font = pygame.font.Font(None, 30)
                playAgain = "To play again press ENTER"
                playAgain_surface = font.render(playAgain, True, (255, 0, 0))
                playAgain_rect = playAgain_surface.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + vertical_position + 30))
                screen.blit(playAgain_surface, playAgain_rect)

                # Ensure we maintain a 30 frames per second rate
                pygame.display.flip()
                clock.tick(30)

                for event in pygame.event.get():
                    # Did the user hit a key?
                    if event.type == KEYDOWN:
                        # Was it the Escape key? If so, stop the loop
                        if event.key == K_ESCAPE:
                            running = True
                            run_game = False

                        if event.key == K_RETURN or event.key == K_KP_ENTER:
                            running = True
                            player.reset()
                            for ob in obstacles:
                                ob.kill()
                            new_obstacle = Obstacle(False)
                            obstacles.add(new_obstacle)
                            for cloud in clouds:
                                cloud.kill()

                    elif event.type == QUIT:
                        running = True
                        run_game = False


if __name__ == '__main__':
    runDoodleJump()
