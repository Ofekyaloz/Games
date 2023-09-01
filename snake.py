import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
game_records = []


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.score = 0
        self.alive = True
        self.direction = 0
        self.lastPosition = self.rect
        self.lastDirection = self.direction
        self.tail = self

    def reset(self):
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.score = 0
        self.alive = True
        self.direction = 0
        self.lastPosition = self.rect
        self.tail = self

    def update(self, pressed_keys):
        # right = 0, left = 1, up = 2, down = 3
        self.lastDirection = self.direction
        self.lastPosition = self.rect.copy()

        if pressed_keys[K_UP] and self.direction != 3:
            self.direction = 2
        if pressed_keys[K_DOWN] and self.direction != 2:
            self.direction = 3
        if pressed_keys[K_LEFT] and self.direction != 0:
            self.direction = 1
        if pressed_keys[K_RIGHT] and self.direction != 1:
            self.direction = 0

        # Keep player on the screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.alive = False
        else:
            x = 15
            if self.direction == 0:
                self.rect.move_ip(x, 0)
            elif self.direction == 1:
                self.rect.move_ip(-x, 0)
            elif self.direction == 2:
                self.rect.move_ip(0, -x)
            else:
                self.rect.move_ip(0, x)


class Tail(pygame.sprite.Sprite):
    def __init__(self, head):
        super(Tail, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = head.lastPosition
        self.head = head
        self.lastPosition = self.rect
        self.direction = head.direction
        self.lastDirection = self.direction

    def update(self):
        self.lastDirection = self.direction
        self.lastPosition = self.rect.copy()
        self.rect = self.head.lastPosition


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super(Apple, self).__init__()
        self.radius = 10
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (self.radius, self.radius), self.radius)  # Draw a red circle
        self.rect = self.surf.get_rect(center=(random.randint(self.radius, SCREEN_WIDTH - self.radius),
                                               random.randint(self.radius, SCREEN_HEIGHT - self.radius)))

    def newPossition(self, tails):
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (self.radius, self.radius), self.radius)  # Draw a red circle
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
all_sprites.add(player)
all_sprites.add(apple)

run_game = True
running = True
pause = False

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

        # Ensure we maintain a 30 frames per second rate
        clock.tick(30)
        continue

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    running = player.alive
    tails.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    # if pygame.sprite.spritecollideany(player, tails):
    #     player.alive = False

    # Check if the new position collides with any tail segment
    # if not any(tail.rect.colliderect(side_rect) for tail in tails):
    #     self.rect = new_rect

    if apple.rect.colliderect(player.rect):
        apple.newPossition(tails)
        player.score += 10
        tail = Tail(player.tail)
        player.tail = tail
        tails.add(tail)
        all_sprites.add(tail)

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

                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = True
                    run_game = False
