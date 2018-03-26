
from os import path
from enum import Enum
from settings import *
import pygame as pg


# Spritesheet object for a .png file
class Spritesheet:

    # Spritesheet constructor
    def __init__(self, filename):
        # Initialize spritesheet attribute as a loaded and converted pygame image
        self.spritesheet = pg.image.load(filename).convert()

    # Method to get an image from the spritesheet
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))  # Create a surface for the image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))  # Blit the image to the surface
        image = pg.transform.scale(image, (GRID_SIZE, GRID_SIZE))  # Scale the image to be the size of a grid square
        return image  # Return image object


# Base class for sprites within the game
class Entity(pg.sprite.Sprite):

    # Entity constructor
    def __init__(self, x, y, image):
        super().__init__()  # Call pygame constructor for sprites

        self.image = image  # Initialize image attribute inherited from pygame Sprite class
        self.rect = self.image.get_rect()  # Get the rect object for the image attribute
        self.rect.x = x  # Set sprite x position
        self.rect.y = y  # Set sprite y position

        self.vy = 0  # Initialize y velocity
        self.vx = 0  # Initialize x velocity

    # Method to apply gravity to an entity
    def apply_gravity(self):
        self.vy += 1.0  # Increase y velocity
        self.vy = min(self.vy, 32)  # Terminal velocity is 32


# Class for platforms in the game
class Platform(Entity):

    # Platform constructor
    def __init__(self, x, y, platformtype):
        self.platformtype = platformtype  # Set the platform type so correct image for type can be loaded
        self.dir = path.dirname(__file__)  # Get file directory
        img_dir = path.join(self.dir, 'img')  # Path to img file
        # Create spritesheet object for platform spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, 'platform_grass_sheet.png'))
        image = self.load_image()  # return image object based on platform type
        super().__init__(x, y, image)  # Call constructor for Entity

    # Return an image object based on the platform type
    def load_image(self):
        return self.spritesheet.get_image(self.platformtype.x, self.platformtype.y, self.platformtype.width,
                                          self.platformtype.height)


# Specify platform types for use in loading images from platform spritesheet
class PlatformType(Enum):
    SQUARE_GRASS = (280, 210, 70, 70)
    BLANK = (70, 280, 70, 70)
    ROUNDED_RIGHT = (210, 140, 70, 70)
    ROUNDED_LEFT = (210, 210, 70, 70)

    # Constructor for a PlatformType
    def __init__(self, x, y, width, height):
        self.x = x  # x position of platform sprite
        self.y = y  # y position of platform sprite
        self.width = width  # width of platform sprite
        self.height = height  # height of platform sprite


# Class for player
class Player(Entity):

    # Player constructor
    def __init__(self):
        self.dir = path.dirname(__file__)  # Get file directory
        img_dir = path.join(self.dir, 'img')  # Path to img file
        # Create spritesheet object for player spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, 'spritesheet_jumper.png'))
        image = self.spritesheet.get_image(690, 406, 120, 201)  # Get image object from spritesheet method
        super().__init__(0 * 32, 19 * 32, image)  # Call constructor for Entity

        self.speed = 3.75  # Player speed attribute initialized as 3.75
        self.jump_power = 15  # Player jump_power attribute initialized as 15

        self.vx = 0  # X velocity attribute initialized as 0
        self.vy = 0  # Y velocity attribute initialized as 0

        self.hearts = MAX_HEARTS

        # Initialize all other attributes
        self.standing_frames = []
        self.walk_frames_l = []
        self.walk_frames_r = []
        self.jump_frames_l = []
        self.jump_frames_r = []
        self.walking = False
        self.on_ground = True
        self.last_update = 0
        self.current_frame = 0
        self.mask = None
        self.images_load()  # Load images for player

    # Populate frame lists with image objects
    def images_load(self):
        self.standing_frames = [self.spritesheet.get_image(690, 406, 120, 201),
                                self.spritesheet.get_image(614, 1063, 120, 191)]
        for frame in self.standing_frames:
            frame.set_colorkey((0, 0, 0))
        self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
                              self.spritesheet.get_image(692, 1458, 120, 207)]
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frames_r = [self.spritesheet.get_image(382, 763, 150, 181)]
        for frame in self.jump_frames_r:
            frame.set_colorkey((0, 0, 0))
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))

    # Animate player sprite
    def animate(self):
        now = pg.time.get_ticks()
        if self.vx != 0:
            self.walking = True
        else:
            self.walking = False
        # Show walk animation
        if self.walking and self.on_ground:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                center = self.rect.center
                if self.vx > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        # Show jump animation
        if not self.on_ground and self.vy < 0:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                center = self.rect.center
                if self.vx < 0:
                    self.image = self.jump_frames_l[self.current_frame]
                else:
                    self.image = self.jump_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

        # Show idle animation
        if self.on_ground and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                center = self.rect.center
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

        # Update mask
        self.mask = pg.mask.from_surface(self.image)

    # Move sprite left
    def move_left(self):
        self.vx = -self.speed

    # Move sprite right
    def move_right(self):
        self.vx = self.speed

    # Stop sprite moving
    def stop(self):
        self.vx = 0

    # Make sprite jump
    def jump(self, platforms):
        self.rect.y += 1

        hit_list = pg.sprite.spritecollide(self, platforms, False)

        # Fall when collision with platform detected
        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power

        self.rect.y -= 1

    # Keep sprite within world boundaries
    def check_world_boundaries(self):
        # Check left side
        if self.rect.left < 0:
            self.rect.left = 0
        # Check right side
        elif self.rect.right > 64 * GRID_SIZE:
            self.rect.right = 64 * GRID_SIZE
        # Check top
        elif self.rect.top < 0:
            self.rect.top = 0

    # Add velocity to position and detect collisions with platforms
    def move_and_process_platforms(self, platforms):
        self.rect.x += self.vx  # Move in x direction
        hit_list = pg.sprite.spritecollide(self, platforms, False)

        for platform in hit_list:
            # Moving right detection
            if self.vx > 0:
                self.rect.right = platform.rect.left   # Place sprite back on left hand side of platform
                self.vx = 0
            # Moving left detection
            elif self.vx < 0:
                self.rect.left = platform.rect.right  # Place sprite back on right hand side of platform
                self.vx = 0

        self.on_ground = False  # Assume sprite not on ground
        self.rect.y += self.vy + 1  # Move in y direction

        hit_list = pg.sprite.spritecollide(self, platforms, False)

        for platform in hit_list:
            # Moving down detection
            if self.vy > 0:
                self.rect.bottom = platform.rect.top  # Place sprite standing on platform
                self.vy = 0
                self.on_ground = True  # Sprite is on the ground (ground defined as any platform)
            # Moving up detection
            elif self.vy < 0:
                self.rect.top = platform.rect.bottom  # Place sprite top at bottom of the platform
                self.vy = 0

    def add_hearts(self, hearts):
        # if hearts > 0:
            # playSound(LVL_UP_SOUND)

        # else:
            # playSound(DMG_SOUND)

        self.hearts += hearts

        if self.hearts > MAX_HEARTS:
            self.hearts = MAX_HEARTS

        elif self.hearts < 0:
            self.die()

    def die(self):
        self.rect.x = 0 * 32
        self.rect.y = 19 * 32
        self.image = self.standing_frames[0]
        self.hearts = MAX_HEARTS

    # Update the player sprite
    def update(self, game):
        self.apply_gravity()  # Apply gravity to player
        self.move_and_process_platforms(game.platforms)  # Move and process collisions with platforms
        self.check_world_boundaries()  # Check sprite still in world boundaries
        self.animate()  # Animate player sprite
