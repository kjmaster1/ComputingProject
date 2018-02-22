
from sprites import *
# Import pygame as pg, This saves time typing throughout coding.
import pygame as pg

# Create Game class, this is class which controls game loop


class Game:

    def __init__(self):
        # Initialize the pygame game window
        pg.init()
        self.screen = pg.display.set_mode((800, 400))
        pg.display.set_caption("Platformer Project")
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.plat2 = Platform(self, 700, 300)
        self.plat3 = Platform(self, 760, 260)
        self.plat4 = Platform(self, 900, 240)
        self.plat5 = Platform(self, 1000, 220)
        self.plat6 = Platform(self, 1100, 200)
        self.plat7 = Platform(self, 1200, 180)
        self.plat8 = Platform(self, 1300, 160)

    def play(self):
        # The Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def draw(self):
        # Drawing to the screen in loop
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        # When drawing is complete you 'flip' the display
        pg.display.flip()

    def events(self):
        # Events in loop
        for event in pg.event.get():
            # check if 'x' being clicked
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        if self.player.rect.left <= 800 / 4:
            self.player.pos.x += max(abs(self.player.vel.x), 0.3)
            for sprite in self.all_sprites:
                if sprite != self.player:
                    sprite.rect.x += int(max(abs(self.player.vel.x), 0.3))

        if self.player.rect.right >= 600:
            self.player.pos.x -= max(abs(self.player.vel.x), 0.3)
            for sprite in self.all_sprites:
                if sprite != self.player:
                    sprite.rect.x -= int(max(abs(self.player.vel.x), 0.3))


game = Game()

while game.running:
    game.play()

pg.quit()
