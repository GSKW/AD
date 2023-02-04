import pygame as pg


class Main:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((600, 600))
        self.clock = pg.time.Clock()
        self.fps = 60
        self.back = (30, 30, 30)
        self.images = {

        }

        self.place_image('images/bed.png', (50, 50), (100, 100))

    def place_image(self, path, size, pos):
        key = path.split('/')[1]
        image = pg.transform.scale(pg.image.load(path), size)
        self.images[key] = [image, pg.Rect(*pos, *size), True]

    def frame(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
            if event.type == pg.MOUSEBUTTONDOWN:
                for name, image in self.images.items():
                    if image[1].collidepoint(event.pos):
                        self.images[name] = [image[0], image[1], False]

        pg.display.flip()
        self.screen.fill(self.back)
        self.clock.tick(self.fps)



        for name, image in self.images.items():
            if image[2]:
                self.screen.blit(*image[:2])




if __name__ == '__main__':
    main = Main()
    while not main.frame():
        pass