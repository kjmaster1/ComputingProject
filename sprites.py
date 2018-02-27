import pygame as pg
from os import path
from enum import Enum


class Spritesheet:

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (64, 64))
        return image


class Entity(pg.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

    def apply_gravity(self):
        self.vy += 1.0
        self.vy = min(self.vy, 32)


class Platform(Entity):

    def __init__(self, x, y, platformtype):
        self.platformtype = platformtype
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, 'platform_grass_sheet.png'))
        image = self.load_image()
        super().__init__(x, y, image)

    def load_image(self):
        if self.platformtype is PlatformType.GROUND:
            return self.spritesheet.get_image(140, 210, 70, 40)
        elif self.platformtype is PlatformType.MID:
            return self.spritesheet.get_image(70, 280, 70, 70)


class Player(Entity):

    def __init__(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, 'player_tilesheet.png'))
        image = self.spritesheet.get_image(10, 14, 61, 96)
        super().__init__(4 * 32, 8 * 32, image)

        self.speed = 5
        self.jump_power = 20

        self.vx = 0
        self.vy = 0

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
        self.images_load()

    def images_load(self):
        self.standing_frames = [self.spritesheet.get_image(10, 14, 61, 96)]
        for frame in self.standing_frames:
            frame.set_colorkey((0, 0, 0))
        self.walk_frames_r = [self.spritesheet.get_image(3, 123, 71, 97),
                              self.spritesheet.get_image(411, 234, 58, 96)]
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frames_r = [self.spritesheet.get_image(84, 9, 71, 100)]
        for frame in self.jump_frames_r:
            frame.set_colorkey((0, 0, 0))
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))

    def animate(self):
        now = pg.time.get_ticks()
        if self.vx != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
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

        if not self.on_ground:
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

        # show idle animation
        if self.on_ground and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                center = self.rect.center
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        self.mask = pg.mask.from_surface(self.image)

    def move_left(self):
        self.vx = -self.speed
        # self.facing_right = False

    def move_right(self):
        self.vx = self.speed
        # self.facing_right = True

    def stop(self):
        self.vx = 0

    def jump(self, platforms):
        self.rect.y += 1

        hit_list = pg.sprite.spritecollide(self, platforms, False)

        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power
            # play_sound(JUMP_SOUND)

        self.rect.y -= 1

    def check_world_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 64 * 64:
            self.rect.right = 64 * 64
        elif self.rect.top < 0:
            self.rect.top = 0

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pg.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.on_ground = False
        self.rect.y += self.vy + 1  # the +1 is hacky. not sure why it helps.
        hit_list = pg.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def update(self, game):
        self.apply_gravity()
        self.move_and_process_blocks(game.platforms)
        self.check_world_boundaries()
        self.animate()


class PlatformType(Enum):
    GROUND = "Ground"
    MID = "Mid"
