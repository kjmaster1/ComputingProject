from sprites import *
from settings import *
import pygame as pg
import json

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
        self.level_test = Level("level_test.json", self)
        self.player = None
        self.active_sprites = pg.sprite.Group()  # Group for active (image changing) sprites
        self.inactive_sprites = pg.sprite.Group()  # Group for inactive (not image changing) sprites
        self.platforms = pg.sprite.Group()  # Group for all platform sprites - used for collision detection
        self.players = pg.sprite.Group()
        self.inactive_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.active_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.level_test.create_level()

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
                    if self.enemy.hurt:
                        self.enemy.hurt = False
                    else:
                        self.enemy.hurt = True

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
        self.active_sprites.update(self)

    # Method to calculate offset of sprites from player
    def calculate_offset(self):
        x = -1 * self.player.rect.centerx + WIDTH / 2  # Assume need to offset by half window size

        if self.player.rect.centerx < WIDTH / 2:  # If player position less than half window size then
            x = 0  # No offset needed
        # If player position more than level width (pixels) - half game window size then
        elif self.player.rect.centerx > (64 * GRID_SIZE) - WIDTH / 2:
            x = -1 * (64 * GRID_SIZE) + WIDTH  # Offset by level width (pixels) + window width

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


class Level:

    def __init__(self, filename, game):
        self.game = game
        self.dir = path.dirname(__file__)  # Get file directory
        lvl_dir = path.join(self.dir, 'levels')  # Path to levels file
        file_path = path.join(lvl_dir, filename)
        self.data = json.load(open(file_path))
        self.playerData = self.data["Player"]
        self.enemiesData = self.data["Enemies"]
        self.platformsData = self.data["Platforms"]
        self.powerupsData = self.data["Powerups"]
        self.length = None
        self.startX = None
        self.startY = None

    def create_level(self):
        self.create_player()
        self.create_platforms()
        self.create_powerups()
        self.create_enemies()

    def create_player(self):
        self.startX = self.playerData["coords"][0]
        self.startY = self.playerData["coords"][1]
        player = Player(self.startX, self.startY)
        self.game.player = player
        self.game.players.add(player)

    def create_platforms(self):
        self.create_floor()
        other_data = self.platformsData["Other"]
        for i in range(0, len(other_data)):
            platform_data = other_data[str(i)]
            coords_data = platform_data["coords"]
            x = coords_data[0]
            y = coords_data[1]
            platform_type_string = platform_data["type"]
            platform_type = PlatformType.get_type_from_string(platform_type_string)
            platform = Platform(x * GRID_SIZE, y * GRID_SIZE, platform_type)
            self.game.platforms.add(platform)
            self.game.inactive_sprites.add(platform)

    def create_enemies(self):
        for i in range(0, len(self.enemiesData)):
            enemy_data = self.enemiesData[str(i)]
            coords_data = enemy_data["coords"]
            x = coords_data[0]
            y = coords_data[1]
            type = enemy_data["type"]
            enemy = Enemy(x * GRID_SIZE, y * GRID_SIZE, self.game.player)
            self.game.active_sprites.add(enemy)

    def create_powerups(self):
        for i in range(0, len(self.powerupsData)):
            powerup_data = self.powerupsData[str(i)]
            coords_data = powerup_data["coords"]
            x = coords_data[0]
            y = coords_data[1]
            type = powerup_data["type"]
            powerup = Powerup(x * GRID_SIZE, y * GRID_SIZE)
            self.game.active_sprites.add(powerup)

    def create_floor(self):
        floor_data = self.platformsData["Floor"]
        gap_data = floor_data["Gaps"]
        self.length = floor_data["length"]
        gaps = []

        for i in range(0, len(gap_data)):
            gaps.append(gap_data[str(i)])

        for i in range(0, self.length):
            if i not in gaps:
                platform = Platform(i * GRID_SIZE, 19 * GRID_SIZE, PlatformType.BLANK)
                self.game.platforms.add(platform)
                self.game.inactive_sprites.add(platform)


# Initialize game
game = Game()
# Game Loop
game.loop()
# Quit pygame + program
pg.quit()
quit()
