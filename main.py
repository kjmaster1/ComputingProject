
from sprites import *
from settings import *
import pygame as pg

pg.mixer.pre_init()
pg.init()


class Game:
    def __init__(self):
        self.window = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.done = False
        self.active_sprites = pg.sprite.Group()
        self.inactive_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def update(self):
        pass  # currently does nothing

    def calculate_offset(self):
        pass  # currently does nothing

    def draw(self):
        self.window.fill(BLACK)
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
