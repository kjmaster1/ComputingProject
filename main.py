
from sprites import *
from settings import *
import pygame as pg

pg.mixer.pre_init()
pg.init()


def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
    if sound_on:
        sound.play(loops, maxtime, fade_ms)


def play_music():
    if sound_on:
        pg.mixer.music.play(-1)


class Game:

    def __init__(self):
        self.window = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.done = False
        self.player = Player()
        self.active_sprites = pg.sprite.Group()
        self.inactive_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        for i in range(0, 64):
            platform = Platform(i * GRID_SIZE, 19 * GRID_SIZE, PlatformType.MID)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(2 * GRID_SIZE, 18 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        for i in range(3, 8):
            platform = Platform(i * GRID_SIZE, 18 * GRID_SIZE, PlatformType.MID)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(3 * GRID_SIZE, 17 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        for i in range(4, 8):
            platform = Platform(i * GRID_SIZE, 17 * GRID_SIZE, PlatformType.MID)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(4 * GRID_SIZE, 16 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        for i in range(5, 8):
            platform = Platform(i * GRID_SIZE, 16 * GRID_SIZE, PlatformType.MID)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(5 * GRID_SIZE, 15 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        for i in range(6, 8):
            platform = Platform(i * GRID_SIZE, 15 * GRID_SIZE, PlatformType.MID)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(6 * GRID_SIZE, 14 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        for i in range(7, 8):
            platform = Platform(i * GRID_SIZE, 14 * GRID_SIZE, PlatformType.MID)
            self.platforms.add(platform)
            self.inactive_sprites.add(platform)

        platform = Platform(7 * GRID_SIZE, 13 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        platform = Platform(9 * GRID_SIZE, 12 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        platform = Platform(11 * GRID_SIZE, 11 * GRID_SIZE, PlatformType.GROUND)
        self.platforms.add(platform)
        self.inactive_sprites.add(platform)

        self.inactive_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.active_layer = pg.Surface([64 * GRID_SIZE, 20 * GRID_SIZE], pg.SRCALPHA, 32)
        self.inactive_sprites.draw(self.inactive_layer)

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            elif event.type == pg.KEYDOWN:

                    if event.key == JUMP:
                        self.player.jump(self.platforms)

        pressed = pg.key.get_pressed()

        if pressed[LEFT]:
            self.player.move_left()
        elif pressed[RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()

    def update(self):
        self.player.update(self)

    def calculate_offset(self):
        x = -1 * self.player.rect.centerx + WIDTH / 2

        if self.player.rect.centerx < WIDTH / 2:
            x = 0
        elif self.player.rect.centerx > (64 * GRID_SIZE) - WIDTH / 2:
            x = -1 * (64 * GRID_SIZE) + WIDTH

        return x, 0

    def draw(self):

        offset_x, offset_y = self.calculate_offset()

        self.window.fill((0, 0, 0))

        self.active_layer.fill(TRANSPARENT)
        self.active_sprites.draw(self.active_layer)

        self.active_layer.blit(self.player.image, [self.player.rect.x, self.player.rect.y])

        self.window.blit(self.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.active_layer, [offset_x, offset_y])

        pg.display.flip()

    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


game = Game()
game.loop()
pg.quit()
quit()
