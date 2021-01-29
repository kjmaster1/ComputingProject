from sprites import *
from settings import *
import pygame as pg
import json

# Kurtis Clements OCR Computer Science A Level Platformer Project
# All assets used fall under the CC license - https://creativecommons.org/publicdomain/zero/1.0/
# Spritesheets were obtained from kenney.nl
# Sounds were obtained from freesound.org
# Two GitHub repos were used for help with this project
# 1) https://github.com/kidscancode/pygame_tutorials/tree/master/platform/working
# https://github.com/kidscancode/pygame_tutorials/blob/master/LICENSE
# 2) https://github.com/joncoop/pygame-platformer/blob/master/game.py
# Any code used from these projects will be commented with a link to the suitable area on GitHub

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
        self.level_one = Level("level_one.json", self)
        self.level_two = Level("level_two.json", self)
        self.level_three = Level("level_three.json", self)
        self.levels = []
        self.levels.append(self.level_one)
        self.levels.append(self.level_two)
        self.levels.append(self.level_three)
        self.player = None
        self.current_level = 0
        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0

        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
        self.carrot_sound = pg.mixer.Sound(path.join(self.snd_dir, 'carrot.wav'))
        self.hurt_player_sound = pg.mixer.Sound(path.join(self.snd_dir, 'hurt_player.wav'))
        self.heart_sound = pg.mixer.Sound(path.join(self.snd_dir, 'heart_sound.wav'))
        self.hurt_enemy_sound = pg.mixer.Sound(path.join(self.snd_dir, 'hurt_enemy.wav'))
        self.active_sprites = None  # Group for active (image changing) sprites
        self.inactive_sprites = None  # Group for inactive (not image changing) sprites
        self.platforms = None  # Group for all platform sprites - used for collision detection
        self.players = None
        self.inactive_layer = None
        self.active_layer = None
        level = self.levels[self.current_level]
        level.create_level()

    # Method to process events retrieved from pygame
    def process_events(self):
        for event in pg.event.get():  # Iterate through events in the pygame event queue
            if event.type == pg.QUIT:  # Done attribute is True when user attempting to quit
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == JUMP:
                    self.player.jump(self)
        pressed = pg.key.get_pressed()

        if pressed[LEFT]:
            self.player.move_left()
        elif pressed[RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()

    # Method to update all sprites
    def update(self):
        level = self.levels[self.current_level]
        level.update()
        self.player.update(self)
        if self.player.rect.right >= 64 * GRID_SIZE:
            level.score = round(self.player.hearts * 1000 - ((level.time / 60) * 10))
            if self.current_level < MAX_LEVELS - 1:
                level.destroy_level()
                self.current_level += 1
                level = self.levels[self.current_level]
                level.create_level()
                self.inactive_sprites.draw(self.inactive_layer)
            else:
                self.show_game_complete()

        self.active_sprites.update(self)

    # https://github.com/joncoop/pygame-platformer/blob/master/game.py#L723
    # Method to calculate offset of sprites from player
    def calculate_offset(self):
        level = self.levels[self.current_level]

        x = -1 * self.player.rect.centerx + WIDTH / 2  # Assume need to offset by half window size

        if self.player.rect.centerx < WIDTH / 2:  # If player position less than half window size then
            x = 0  # No offset needed
        # If player position more than level width (pixels) - half game window size then
        elif self.player.rect.centerx > (level.length * GRID_SIZE) - WIDTH / 2:
            x = -1 * (level.length * GRID_SIZE) + WIDTH  # Offset by level width (pixels) + window width

        return x, 0  # Return the calculated offset

    # https://github.com/joncoop/pygame-platformer/blob/master/game.py#L733 with added draw_text calls
    # Method to draw all sprites to window
    def draw(self):
        offset_x, offset_y = self.calculate_offset()
        self.window.fill(LIGHT_BLUE)  # Fill window with black background
        self.active_layer.fill(TRANSPARENT)
        self.active_sprites.draw(self.active_layer)

        self.active_layer.blit(self.player.image, [self.player.rect.x, self.player.rect.y])

        self.window.blit(self.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.active_layer, [offset_x, offset_y])

        level = self.levels[self.current_level]
        self.draw_text("Time: " + str(round(level.time / 60)), 22, WHITE, 64, 50)
        hearts = self.player.hearts
        self.draw_text("Hearts: " + str(hearts), 22, WHITE, 64, 30)
        pg.display.flip()  # 'Flip' display

    # Method for main game loop
    def loop(self):
        while not self.done:  # While game not done being played
            self.process_events()  # First process events
            self.update()  # Then, update all sprites
            self.draw()  # Next, draw all sprites
            self.clock.tick(FPS)  # Finally, ensure game loop running at 60 FPS.

    # https://github.com/kidscancode/pygame_tutorials/blob/master/platform/working/main.py#L164
    # Show the main menu
    def show_main_menu(self):
        self.window.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow Keys to move", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    # Show the game completed screen
    def show_game_complete(self):
        self.window.fill(BLACK)
        self.draw_text("Game Complete!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        score = 0
        for level in self.levels:
            score += level.score
        self.draw_text("Score: " + str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to quit", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if score > self.highscore:
            self.highscore = score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, "highscore.txt"), 'w') as f:
                f.write(str(score))  # New high score is written to file
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()  # Wait for key twice here as user is likely to have a key pressed down when screen appears
        self.wait_for_key()
        pg.quit()
        quit()

    # https://github.com/kidscancode/pygame_tutorials/blob/master/platform/working/main.py#L198
    # Wait for a key input from user before program continues
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.done = True
                if event.type == pg.KEYUP:  # When a key is released we are no longer waiting for user
                    waiting = False

    # https://github.com/kidscancode/pygame_tutorials/blob/master/platform/working/main.py#L209
    # Draw text to the window
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.window.blit(text_surface, text_rect)


class Level:

    # Level class constructor
    def __init__(self, filename, game):
        self.game = game
        self.dir = path.dirname(__file__)  # Get file directory
        self.snd_dir = path.join(self.dir, 'snd')
        lvl_dir = path.join(self.dir, 'levels')  # Path to levels file
        file_path = path.join(lvl_dir, filename)
        self.data = json.load(open(file_path))
        # Split data dictionary up with each key
        self.player_data = self.data["Player"]
        self.enemies_data = self.data["Enemies"]
        self.platforms_data = self.data["Platforms"]
        self.powerups_data = self.data["Powerups"]
        self.length = None
        self.start_x = None
        self.start_y = None
        self.time = 0
        self.score = 0
        self.music_data = self.data["Music"]
        self.music_file = self.music_data["file"]  # Retrieve file path to music for the level

    # Create a level by calling the other methods, creating the inactive surface, drawing inactive sprites and playing music
    def create_level(self):
        self.game.active_sprites = pg.sprite.Group()  # Group for active (image changing) sprites
        self.game.inactive_sprites = pg.sprite.Group()  # Group for inactive (not image changing) sprites
        self.game.platforms = pg.sprite.Group()
        self.game.players = pg.sprite.Group()
        self.game.inactive_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.game.active_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.create_player()
        self.create_platforms()
        self.create_powerups()
        self.create_enemies()
        self.game.inactive_sprites.draw(self.game.inactive_layer)
        pg.mixer.music.load(path.join(self.snd_dir, self.music_file))
        pg.mixer.music.play(loops=-1)

    # Create a new player instance at the co-ords specified
    def create_player(self):
        self.start_x = self.player_data["coords"][0]
        self.start_y = self.player_data["coords"][1]
        player = Player(self.start_x, self.start_y)
        self.game.player = player
        self.game.players.add(player)

    # Create instances of platform at the co-ords specified with the specified platformtype
    def create_platforms(self):
        self.create_floor()
        other_data = self.platforms_data["Other"]
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

    # Create instances of the correct enemy based on the type and at the co-ords specified
    def create_enemies(self):
        for i in range(0, len(self.enemies_data)):
            enemy_data = self.enemies_data[str(i)]
            coords_data = enemy_data["coords"]
            x = coords_data[0]
            y = coords_data[1]
            enemy_type = enemy_data["type"]

            if enemy_type == "flying":
                enemy = Flying(x * GRID_SIZE, y * GRID_SIZE, self.game.player)
            elif enemy_type == "worm":
                enemy = Worm(x * GRID_SIZE, y * GRID_SIZE, self.game.player)
            else:
                enemy = Basic(x * GRID_SIZE, y * GRID_SIZE, self.game.player)

            self.game.active_sprites.add(enemy)

    # Create instances of the correct powerup based on the type and at the co-ords specified
    def create_powerups(self):
        for i in range(0, len(self.powerups_data)):
            powerup_data = self.powerups_data[str(i)]
            coords_data = powerup_data["coords"]
            x = coords_data[0]
            y = coords_data[1]
            powerup_type = powerup_data["type"]

            if powerup_type == "gold_carrot":
                powerup = GoldCarrot(x * GRID_SIZE, y * GRID_SIZE)
            else:
                powerup = Carrot(x * GRID_SIZE, y * GRID_SIZE)

            self.game.active_sprites.add(powerup)

    # Create the floor of the level by creating instances of blank platforms and leaving out any gaps specified
    def create_floor(self):
        floor_data = self.platforms_data["Floor"]
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

    # 'Destroy' the level by using the kill method on all the sprites and moving them to 0,0
    def destroy_level(self):
        pg.mixer.music.fadeout(500)
        for sprite in self.game.active_sprites:
            sprite.kill()
            sprite.rect.x = 0
            sprite.rect.y = 0
        for sprite in self.game.inactive_sprites:
            sprite.kill()
            sprite.rect.x = 0
            sprite.rect.y = 0
        for sprite in self.game.platforms:
            sprite.kill()
            sprite.rect.x = 0
            sprite.rect.y = 0
        for sprite in self.game.players:
            sprite.kill()
            sprite.rect.x = 0
            sprite.rect.y = 0

    # Increment time
    def update(self):
        self.time += 1


# Initialize game
game = Game()
# Menu
game.show_main_menu()
# Game Loop
game.loop()
# Quit pygame + program
pg.quit()
quit()
