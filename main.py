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

    def play(self):
        # The Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.draw()

    def draw(self):
        # Drawing to the screen in loop
        self.screen.fill((0, 0, 0))
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


game = Game()

while game.running:
    game.play()

pg.quit()
