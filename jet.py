import pygame
import random
from pygame.locals import *

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
game_records = []


# Define the Player object extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(0,SCREEN_HEIGHT // 2))
        self.score = 0
        self.lives = 3

    def reset(self):
        self.rect = self.surf.get_rect(center=(0, SCREEN_HEIGHT // 2))
        self.score = 0
        self.lives = 3

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-8, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        self.angle = random.randint(-2, 2)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, self.angle)
        if self.rect.right < 0 or self.rect.top < -10 or self.rect.bottom > SCREEN_HEIGHT + 10:
            self.kill()
            player.score += 5


class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super(Heart, self).__init__()
        self.surf = pygame.image.load("heart.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 25, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
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


pygame.mixer.init()
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDHEART = pygame.USEREVENT + 3
pygame.time.set_timer(ADDHEART, 10000)
# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
hearts = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(2)

# Variable to keep our main loop running
running = True
sound = True
pause = False
run_game = True

# Our main loop
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
                    pygame.time.set_timer(ADDENEMY, 0)
                    pygame.time.set_timer(ADDCLOUD, 0)
                    pygame.time.set_timer(ADDHEART, 0)
                else:
                    pygame.time.set_timer(ADDENEMY, 250)
                    pygame.time.set_timer(ADDCLOUD, 1000)
                    pygame.time.set_timer(ADDHEART, 10000)

            if event.key == K_m:
                if sound:
                    pygame.mixer.music.stop()
                    move_up_sound.set_volume(0)
                    move_down_sound.set_volume(0)
                    collision_sound.set_volume(0)
                else:
                    pygame.mixer.music.play()
                    move_up_sound.set_volume(0.5)
                    move_down_sound.set_volume(0.5)
                    collision_sound.set_volume(0.5)

                sound = not sound



        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            run_game = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDHEART:
            new_heart = Heart()
            hearts.add(new_heart)
            all_sprites.add(new_heart)

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

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()
    hearts.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):

        player.lives -= 1

        if player.lives > 0:
            pygame.sprite.spritecollideany(player, enemies).kill()
            collision_sound.play()
        else:
            # Stop any moving sounds and play the collision sound
            move_up_sound.stop()
            move_down_sound.stop()
            collision_sound.play()

            # Stop the loop
            running = False

    if pygame.sprite.spritecollideany(player, hearts):
        pygame.sprite.spritecollideany(player, hearts).kill()
        player.lives += 1

    font = pygame.font.Font(None, 40)
    text = font.render("Score: " + str(player.score), True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 - 100, 30))
    screen.blit(text, text_rect)
    text = font.render("Lives:" + str(player.lives), True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 + 100, 30))
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
                #     score_rect = score_surface.get_rect(topleft=(10, vertical_position))
                screen.blit(score_surface, score_rect)
                vertical_position += 30

            font = pygame.font.Font(None, 40)
            playAgain = "To play again press ENTER"
            playAgain_surface = font.render(playAgain, True, (255, 0, 0))
            playAgain_rect = playAgain_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + vertical_position + 30))
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
                        for enemy in enemies:
                            enemy.kill()
                        for cloud in clouds:
                            cloud.kill()
                        for heart in hearts:
                            heart.kill()

                    if event.key == K_m:
                        if sound:
                            pygame.mixer.music.stop()
                            move_up_sound.set_volume(0)
                            move_down_sound.set_volume(0)
                            collision_sound.set_volume(0)
                        else:
                            pygame.mixer.music.play()
                            move_up_sound.set_volume(0.5)
                            move_down_sound.set_volume(0.5)
                            collision_sound.set_volume(0.5)

                        sound = not sound



                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = True
                    run_game = False

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
