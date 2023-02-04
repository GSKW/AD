import pygame as pg
import csv


class Bar:
    def __init__(self, x, y):
        self.b_pos = (x, y)
        self.b_size = (20, 300)
        self.perc = 0.15
        self.bar = pg.Rect(self.b_pos[0], self.b_pos[1], self.b_size[0], self.b_size[1])
        self.add_bar = pg.Rect(self.b_pos[0] + 1, self.b_pos[1] + 1, self.b_size[0] - 2,
                               (self.b_size[1] - 2) * (1 - self.perc))

class Main:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((600, 600))
        self.back = (30, 30, 30)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.h = 2.0
        self.w_h = 0.6

        self.bar = Bar(520, 150)
        self.w_bar = Bar(400, 150)

        self.add_bar = None
        self.w_add_bar = None

        self.wall_pos = (70, 430)
        self.wall_size = [20]*2

        self.wall_dict = {

            'large_window': [pg.Rect(25, 535, 40, 40), False],
            'exit': [pg.Rect(360, 530, 210, 45), False]
        }

        self.lines = [
            pg.Rect(330, 0, 1, self.screen.get_size()[1]),
            pg.Rect(0, 500, 600, 1),
        ]

        self.bar_stat_1 = 0
        self.bar_stat_2 = 0

    def draw_text(self, surf, text, size, x, y, color):
        font = pg.font.Font(pg.font.match_font('Times New Roman'), size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def frame(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.bar.bar.collidepoint(event.pos):
                    self.bar.perc = (self.screen.get_size()[1] - event.pos[1] - 150) / self.bar.b_size[1]
                if self.w_bar.bar.collidepoint(event.pos):
                    self.w_bar.perc = (self.screen.get_size()[1] - event.pos[1] - 150) / self.w_bar.b_size[1]
                for name, button in self.wall_dict.items():
                    if button[0].collidepoint(event.pos):
                        self.wall_dict[name] = [button[0], not button[1]]
                        if name == 'exit':
                            with open('features.csv', 'w', encoding='utf-8') as file:
                                writer = csv.writer(file, lineterminator='\n')
                                writer.writerow([self.bar_stat_1, self.bar_stat_2, int(self.wall_dict['large_window'][1])])
                            return True
        pg.display.flip()
        self.screen.fill(self.back)
        self.clock.tick(self.fps)

        self.add_bar = pg.Rect(self.bar.b_pos[0] + 1, self.bar.b_pos[1] + 1, self.bar.b_size[0] - 2,
                               (self.bar.b_size[1] - 2) * (1 - self.bar.perc))
        self.w_add_bar = pg.Rect(self.w_bar.b_pos[0] + 1, self.w_bar.b_pos[1] + 1, self.w_bar.b_size[0] - 2,
                               (self.w_bar.b_size[1] - 2) * (1 - self.w_bar.perc))

        self.bar_stat_1 = float(str(self.h*self.bar.perc+2)[:3])
        self.bar_stat_2 = float(str(self.w_h * self.w_bar.perc + 0.5)[:3])

        self.draw_text(self.screen, f'{self.bar_stat_1} m', 20,
                       self.bar.b_pos[0]+10, self.bar.b_pos[1]-50, 'lightblue')
        self.draw_text(self.screen, f'{self.bar_stat_2} m', 20,
                       self.w_bar.b_pos[0] + 10, self.w_bar.b_pos[1] - 50, 'lightblue')

        self.draw_text(self.screen, 'Large windows', 30, 190, 540, 'white')

        self.draw_text(self.screen, 'Wall', 30, 530, 10, 'white')
        self.draw_text(self.screen, 'height', 30, 530, 50, 'white')

        self.draw_text(self.screen, 'Window', 30, 410, 10, 'white')
        self.draw_text(self.screen, 'height', 30, 410, 50, 'white')

        pg.draw.rect(self.screen, 'lightblue', self.bar.bar)
        pg.draw.rect(self.screen, self.back, self.add_bar)

        pg.draw.rect(self.screen, 'lightblue', self.w_bar.bar)
        pg.draw.rect(self.screen, self.back, self.w_add_bar)

        self.draw_text(self.screen, '--->', 60, 470, 522, 'white')

        for name, button in self.wall_dict.items():
            pg.draw.rect(self.screen, 'lightblue', button[0], not int(button[1]))

        for line in self.lines:
            pg.draw.rect(self.screen, 'white', line)


if __name__ == '__main__':
    main = Main()
    while not main.frame():
        pass