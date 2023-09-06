import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
game_records = []
pygame.init()

def runFlappyBird():
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.player_images = {
                0: pygame.image.load("yellowbird-downflap.png").convert(),
                1: pygame.image.load("yellowbird-midflap.png").convert(),
                2: pygame.image.load("yellowbird-upflap.png").convert(),
            }
            self.surf = self.player_images[0]
            self.rect = self.surf.get_rect(center=(50, SCREEN_HEIGHT // 2))
            self.score = 0
            self.alive = True
            self.pic = 0
            self.rotation_angle = 0

        def reset(self):
            self.rect = self.surf.get_rect(center=(50, SCREEN_HEIGHT // 2))
            self.score = 0
            self.alive = True
            self.rotation_angle = 0
            self.surf = self.player_images[0]
            self.surf = pygame.transform.rotate(self.surf, self.rotation_angle)
            self.pic = 0

        def update(self, pressed_keys):
            x = 5
            self.pic += 1
            self.surf = self.player_images[self.pic % 3]
            if pressed_keys[K_SPACE]:
                if self.rotation_angle < 0:
                    self.rotation_angle = 0
                elif self.rotation_angle < 20:
                    self.rotation_angle += 1

                self.rect.move_ip(0, -x * 2)
            else:
                if self.rotation_angle <= 0:
                    self.rotation_angle -= 1
                else:
                    self.rotation_angle = 0

                self.rect.move_ip(0, x)
            self.surf = pygame.transform.rotate(self.surf, self.rotation_angle)

            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT:
                self.alive = False

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            super(Obstacle, self).__init__()
            topHeight = bottomHeight = 0
            while True:
                topHeight = random.randint(60, SCREEN_HEIGHT - 200)
                bottomHeight = random.randint(0, topHeight - 59)
                if SCREEN_HEIGHT // 2 <= topHeight + bottomHeight + 60 <= SCREEN_HEIGHT:
                    break

            self.surfTop = pygame.image.load("pipe-green.png").convert()
            self.surfTop = pygame.transform.rotate(self.surfTop, 180)
            self.surfTop.set_colorkey((255, 255, 255), RLEACCEL)
            self.surfTop = pygame.transform.scale(self.surfTop, (30, topHeight))
            self.rectTop = self.surfTop.get_rect(topleft=(SCREEN_WIDTH + 50, 0))

            self.surfBottom = pygame.image.load("pipe-green.png").convert()
            self.surfBottom.set_colorkey((255, 255, 255), RLEACCEL)
            self.surfBottom = pygame.transform.scale(self.surfBottom, (30, bottomHeight))
            self.rectBottom = self.surfBottom.get_rect(bottomleft=(SCREEN_WIDTH + 50, SCREEN_HEIGHT))

            self.score = False

        def update(self):
            self.rectTop.move_ip(-5, 0)
            self.rectBottom.move_ip(-5, 0)

            if not self.score and self.rectTop.right < 50:
                player.score += 1
                self.score = True

            if self.rectTop.right < 0:
                self.kill()

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("cloud.png").convert()
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
    pygame.display.set_caption('Flappy Bird by Ofek')

    ADDOBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDOBSTACLE, 1100)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1500)

    obstacles = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    player = Player()

    run_game = True
    running = True
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
                new_obstacle = Obstacle()
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
        obstacles.update()
        clouds.update()

        screen.fill((135, 206, 250))

        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rectTop) or player.rect.colliderect(obstacle.rectBottom):
                player.alive = False

        for cloud in clouds:
            screen.blit(cloud.surf, cloud.rect)

        for entity in obstacles:
            screen.blit(entity.surfTop, entity.rectTop)
            screen.blit(entity.surfBottom, entity.rectBottom)

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
                            for cloud in clouds:
                                cloud.kill()


                    # Did the user click the window close button? If so, stop the loop
                    elif event.type == QUIT:
                        running = True
                        run_game = False
