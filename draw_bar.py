import pygame as pg
import sys



def get_path():
    return __file__

class ProgressBar:
    def __init__(self):
        pg.init()
        self.height = 60
        self.width = 240
        self.screen = pg.display.set_mode((self.width, self.height), pg.NOFRAME)
        self.screen.fill((30,30,30))
        self.fps=30
        self.clock = pg.time.Clock()
        self.progress = 0

    def DrawBar(self, pos, size, borderC, barC, progress):
        pg.draw.rect(self.screen, borderC, (*pos, *size), 1)
        innerPos = (pos[0] + 3, pos[1] + 3)
        innerSize = ((size[0] - 6) * progress, size[1] - 6)
        pg.draw.rect(self.screen, barC, (*innerPos, *innerSize))
    def frame(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return True

        pg.draw.rect(self.screen, 'white', pg.Rect(1,1,self.width-1,self.height-1), 1)

        if self.progress < 1000:
            self.progress += 5
            self.DrawBar((20, 20), (200, 20), (0, 0, 0), (0, 128, 0), (self.progress // 10) / 99)
        else:
            pg.quit()
            return True

        pg.display.flip()
        self.clock.tick(self.fps)



if __name__ == '__main__':
    progress_bar = ProgressBar()
    while not progress_bar.frame():
        pass
