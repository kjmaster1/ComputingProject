from sprites import *
from settings import *
import pygame as pg

# Initialize mixer for music
pg.mixer.pre_init()
# Initialize pygame modules
pg.init()


class Game:

    # Game class constructor
    def __init__(self):
        self.window = pg.display.set_mode([WIDTH, HEIGHT])  # Initialize window
        pg.display.set_caption(TITLE)  # Set title of window
        self.clock = pg.time.Clock()  # Initialize clock
        self.done = False  # Done attribute initialized to False
        self.player = Player()
        self.active_sprites = pg.sprite.Group()  # Group for active (moving) sprites
        self.inactive_sprites = pg.sprite.Group()  # Group for inactive (not moving) sprites
        self.platforms = pg.sprite.Group()  # Group for all platform sprites - used for collision detection
        for i in range(0, 64):
            platform = Platform(i * GRID_SIZE, 19 * GRID_SIZE, PlatformType.BLANK)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(10 * GRID_SIZE, 17 * GRID_SIZE, PlatformType.ROUNDED_LEFT)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        platform = Platform(11 * GRID_SIZE, 17 * GRID_SIZE, PlatformType.SQUARE_GRASS)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        platform = Platform(12 * GRID_SIZE, 17 * GRID_SIZE, PlatformType.ROUNDED_RIGHT)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        self.inactive_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.active_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.inactive_sprites.draw(self.inactive_layer)

    # Method to process events retrieved from pygame
    def process_events(self):
        for event in pg.event.get():  # Iterate through events in the pygame event queue
            if event.type == pg.QUIT:  # Done attribute is True when user attempting to quit
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == JUMP:
                    self.player.jump(self.platforms)
                if event.key == pg.K_h:  # FOR TESTING REMOVE ONCE ENEMY ADDED
                    self.player.add_hearts(-1)

        pressed = pg.key.get_pressed()

        if pressed[LEFT]:
            self.player.move_left()
        elif pressed[RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()

    # Method to update all sprites
    def update(self):
        self.player.update(self)

    # Method to calculate offset of sprites from player
    def calculate_offset(self):
        x = -1 * self.player.rect.centerx + WIDTH / 2  # Assume need to offset by half window size

        if self.player.rect.centerx < WIDTH / 2:  # If player position less than half window size then
            x = 0  # No offset needed
        # If player position more than level width (pixels) - half game window size then
        elif self.player.rect.centerx > (64 * GRID_SIZE) - WIDTH / 2:
            x = -1 * (64 * GRID_SIZE) + WIDTH  # Offset by level width (pixels) + window width
            print("Offset by level width + window width")

        return x, 0  # Return the calculated offset

    # Method to draw all sprites to window
    def draw(self):
        offset_x, offset_y = self.calculate_offset()
        self.window.fill(BLACK)  # Fill window with black background
        self.active_layer.fill(TRANSPARENT)
        self.active_sprites.draw(self.active_layer)

        self.active_layer.blit(self.player.image, [self.player.rect.x, self.player.rect.y])

        self.window.blit(self.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.active_layer, [offset_x, offset_y])
        pg.display.flip()  # 'Flip' display

    # Method for main game loop
    def loop(self):
        while not self.done:  # While game not done being played
            self.process_events()  # First process events
            self.update()  # Then, update all sprites
            self.draw()  # Next, draw all sprites
            self.clock.tick(FPS)  # Finally, ensure game loop running at 60 FPS.


# Initialize game
game = Game()
# Game Loop
game.loop()
# Quit pygame + program
pg.quit()
quit()

