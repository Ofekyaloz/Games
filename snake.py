import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
game_records = []


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.player_images = {
            "up": pygame.image.load("snake_up.png").convert(),
            "down": pygame.image.load("snake_down.png").convert(),
            "left": pygame.image.load("snake_left.png").convert(),
            "right": pygame.image.load("snake_right.png").convert(),
        }
        self.surf = self.player_images["right"]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.score = 0
        self.alive = True
        self.direction = "right"
        self.lastPosition = self.rect
        self.lastDirection = self.direction
        self.tail = self

    def reset(self):
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.score = 0
        self.alive = True
        self.direction = "right"
        self.surf = self.player_images["right"]
        self.lastPosition = self.rect
        self.tail = self

    def update(self, pressed_keys):
        self.lastDirection = self.direction
        self.lastPosition = self.rect.copy()

        if pressed_keys[K_UP] and self.direction != "down":
            self.direction = "up"
            self.surf = self.player_images["up"]
        if pressed_keys[K_DOWN] and self.direction != "up":
            self.direction = "down"
            self.surf = self.player_images["down"]
        if pressed_keys[K_LEFT] and self.direction != "right":
            self.direction = "left"
            self.surf = self.player_images["left"]
        if pressed_keys[K_RIGHT] and self.direction != "left":
            self.direction = "right"
            self.surf = self.player_images["right"]

        # Keep player on the screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.alive = False
        else:
            x = 15
            if self.direction == "right":
                self.rect.move_ip(x, 0)
            elif self.direction == "left":
                self.rect.move_ip(-x, 0)
            elif self.direction == "up":
                self.rect.move_ip(0, -x)
            else:
                self.rect.move_ip(0, x)


class Tail(pygame.sprite.Sprite):
    def __init__(self, head):
        super(Tail, self).__init__()
        self.size = 25  # Set the size of the tail segment
        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Draw a circular body with black outline
        pygame.draw.circle(self.surf, (0, 0, 0), (self.size // 2, self.size // 2), self.size // 2)
        pygame.draw.circle(self.surf, (97, 151, 72), (self.size // 2, self.size // 2), self.size // 2 - 2)

        self.rect = head.lastPosition
        self.head = head
        self.lastPosition = self.rect

        # another view
        # self.surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        # pygame.draw.circle(self.surf, (0, 0, 0, 255), (15, 15), 15)
        # pygame.draw.rect(self.surf, (97, 151, 72), (0, 10, 30, 10))
        # pygame.draw.rect(self.surf, (97, 151, 72), (10, 0, 10, 30))


    def update(self):
        self.lastPosition = self.rect.copy()
        self.rect = self.head.lastPosition


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super(Apple, self).__init__()
        self.surf = pygame.image.load("apple.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.radius = 10
        self.rect = self.surf.get_rect(center=(random.randint(self.radius, SCREEN_WIDTH - self.radius),
                                               random.randint(self.radius, SCREEN_HEIGHT - self.radius)))

    def newPossition(self, tails):
        while True:
            new_rect = self.surf.get_rect(center=(random.randint(self.radius, SCREEN_WIDTH - self.radius),
                                                  random.randint(self.radius, SCREEN_HEIGHT - self.radius)))
            if not any(tail.rect.colliderect(new_rect) for tail in tails) and not player.rect.colliderect(new_rect):
                self.rect = new_rect
                break


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game by Ofek')

AddApple = pygame.USEREVENT + 1
player = Player()
apple = Apple()

tails = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(apple)
all_sprites.add(player)

run_game = True
running = True
pause = False

first_tails = []

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


        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            run_game = False

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
    tails.update()

    screen.fill((119, 136, 153))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    for tail in tails:
        if tail in first_tails:
            continue
        if player.rect.colliderect(tail.rect):
            player.alive = False

    if apple.rect.colliderect(player.rect):
        apple.newPossition(tails)
        player.score += 10
        tail = Tail(player.tail)
        player.tail = tail
        tails.add(tail)
        if player.score != 10:
            all_sprites.add(tail)
        else:
            all_sprites.remove(player)
            all_sprites.add(tail)
            all_sprites.add(player)
        if len(first_tails) < 3:
            first_tails.append(tail)

    font = pygame.font.Font(None, 40)
    text = font.render("Score: " + str(player.score), True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(text, text_rect)

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

    if not running:
        game_records.append(player.score)
        game_records.sort(reverse=True)
        if len(game_records) > 10:
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
                if i < 10:
                    i = '0' + str(i)
                score_text = "{}. {}".format(i, score)
                score_surface = font.render(score_text, True, (0, 0, 0))
                score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + vertical_position))
                screen.blit(score_surface, score_rect)
                vertical_position += 30

            font = pygame.font.Font(None, 40)
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
                        apple.newPossition([])
                        for tail in tails:
                            tail.kill()
                        first_tails = []

                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = True
                    run_game = False
