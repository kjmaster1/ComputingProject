import pygame as pg
from os import path
vec = pg.math.Vector2


class Spritesheet:

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, 'player_tilesheet.png'))
        self.image = self.spritesheet.get_image(10, 14, 61, 96)
        self.layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 200)
        self.pos = vec(400, 200)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.jumping = False
        self.standing_frames = []
        self.walk_frames_l = []
        self.walk_frames_r = []
        self.jump_frames_l = []
        self.jump_frames_r = []
        self.walking = False
        self.last_update = 0
        self.current_frame = 0
        self.mask = None
        self.images_load()
        self.game = game

    def update(self):
        self.animate()
        self.acc = vec(0, 0.8)

        if self.pos.y >= 400:
            self.vel.y = 0
            self.jumping = False
            self.pos.y = 400

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -0.5
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.5
        if keys[pg.K_UP]:
            if self.pos.y == 400:
                self.jumping = True
                self.vel.y = -15
            else:
                # jump if standing on a platform
                self.rect.y += 2
                hits = pg.sprite.spritecollide(self, self.game.platforms, False)
                self.rect.y -= 2
                if hits and not self.jumping:
                    self.jumping = True
                    self.vel.y = -15

        # apply friction
        self.acc.x += self.vel.x * -0.12

        # equations of motion
        self.vel.x += self.acc.x
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos.x += self.vel.x + 0.5 * self.acc.x

        self.rect.x = self.pos.x

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            for hit in hits:
                if self.vel.x > 0 and self.pos.y != hit.rect.top:
                    self.pos.x = hit.rect.left - self.rect.width
                    self.vel.x = 0
                    self.rect.x = self.pos.x
                if self.vel.x < 0 and self.pos.y != hit.rect.top:
                    self.pos.x = hit.rect.right
                    self.vel.x = 0
                    self.rect.x = self.pos.x

        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y

        self.rect.y = (self.pos.y - self.rect.height)

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            for hit in hits:
                if self.rect.top + 15 > hit.rect.bottom:
                    self.rect.top = hit.rect.bottom
                    self.vel.y = 0
                    self.jumping = False

                elif self.vel.y > 0 and self.pos.y > hit.rect.top \
                        and hit.rect.right + 18 > self.pos.x > hit.rect.left - 30:
                    self.pos.y = hit.rect.top
                    self.vel.y = 0
                    self.jumping = False

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
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking and not self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.jump_frames_l[self.current_frame]
                else:
                    self.image = self.jump_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


class Platform(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, 'platform_grass_sheet.png'))
        self.image = self.spritesheet.get_image(0, 0, 70, 40)
        self.layer = 1
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)






