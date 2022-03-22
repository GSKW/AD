""" Модуль фронтенда 2 """

import csv
import pygame as pg


class Main:
    """ Главный класс приложения """

    def __init__(self):

        # Инициализация pygame
        pg.init()
        pg.display.set_caption("Auto Design")

        # Создание поверхности экрана
        self.screen = pg.display.set_mode((1400, 700))
        self.width = self.screen.get_size()[0]
        self.height = self.screen.get_size()[1]
        self.multiple = 1.425

        # Загрузка и форматирование изображений
        self.window = pg.transform.scale(pg.image.load('images/wnd.png'), (80, 80))
        self.window.convert()

        self.door = pg.transform.scale(pg.image.load('images/door.png'), (70, 70))
        self.door.convert()

        self.wall = pg.transform.scale(pg.image.load('images/wall.png'), (70, 70))
        self.wall.convert()

        self.clear = pg.transform.scale(pg.image.load('images/bin.png'), (90, 90))
        self.clear.convert()

        self.back = pg.transform.scale(pg.image.load('images/back.png'), (65, 65))
        self.back.convert()

        self.empty = pg.transform.scale(pg.image.load('images/empt.png'), (65, 65))
        self.empty.convert()

        self.ddd = pg.transform.scale(pg.image.load('images/dots.png'), (65, 65))
        self.ddd.convert()

        self.chair = pg.transform.scale(pg.image.load('images/chair.png'), (72, 72))
        self.chair.convert()

        self.table = pg.transform.scale(pg.image.load('images/table.png'), (67, 67))
        self.table.convert()

        self.night = pg.transform.scale(pg.image.load('images/nightstand.png'), (65, 65))
        self.night.convert()

        self.bed = pg.transform.scale(pg.image.load('images/bed.png'), (95, 95))
        self.bed.convert()

        self.closet = pg.transform.scale(pg.image.load('images/closet.png'), (60, 60))
        self.closet.convert()


        # Таймер
        self.clock = pg.time.Clock()

        # Флаг вкладки
        self.pg = True

        # Количество кадров в секунду
        self.fps = 30

        # Переменные для расчета
        self.x = 10
        self.y = 10

        # Словарь цветов
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
              'red': (255, 0, 0),
            'green': (0, 255, 0),
             'blue': (0, 0, 255),
            'not_hovered': 'dodgerblue2',
            'hovered': 'lightskyblue3',
        }

        # Имена изменяемых кнопок
        self.names = ['wall', 'door', 'window', 'empty']

        # Словарь с последними изменениями
        self.last_change = []

        # Словари и переменные для режима dot-to-dot
        self.dots = {}
        self.dot = (0,0)
        self.dot_to_dot = False

        # Массив изображений
        self.images = {}
        self.load_images()

        # Словарь кнопок
        self.buttons = {

            # 265 70
            'clear':pg.Rect(self.width-710,20,70,70),
            'wall': pg.Rect(self.width-710, 150, 70, 70),
            'window': pg.Rect(self.width-710, 300, 70, 70),
            'door': pg.Rect(self.width-710, 450, 70, 70),
            'empty': pg.Rect(self.width - 710, 600, 70, 70),

            'back': pg.Rect(self.width-310, 450, 70, 70),
            'dtd': pg.Rect(self.width-310, 350, 70, 70),

            'generate': pg.Rect(self.width-275, 600, 200, 70),

            'pg1': pg.Rect(self.width - 325, 150, 300, 70),
            'pg2': pg.Rect(self.width - 325, 50, 300, 70),

            '1': pg.Rect(self.width-710, 20, 70, 70),
            '2': pg.Rect(self.width-710, 150, 70, 70),
            '3': pg.Rect(self.width-710, 300, 70, 70),
            '4': pg.Rect(self.width-710, 450, 70, 70),
            '5': pg.Rect(self.width-710, 600, 70, 70),
        }

        # Словарь активности кнопок
        self.buttons_active = {
            '1': False,
            '2': False,
            '3': False,
            '4': False,
            '5': False,
        }
        self.walls = True

        # Словарь цветов изображаемой мебели
        self.furn_colors = {
            '1':'red',
            '2': 'purple',
            '3': 'brown',
            '4': 'blue',
            '5': 'darkgreen',
        }

        # Размер мебели на холсте
        self.furn_size = {
            '1': (25, 25),
            '2': (80, 80),
            '3': (25, 25),
            '4': (80, 100),
            '5': (80, 30),
        }

        # Список мебели на холсте
        self.dictionary = []

        # Холст
        self.canvas = {
            'can': self.gen_canvas((self.screen.get_size()[0] / 3 * self.multiple,
                                    self.screen.get_size()[1])),
            'rect': pg.Rect(0, 0,
                            self.screen.get_size()[0] / 3 * self.multiple,
                            self.screen.get_size()[1])
        }

        # Массив координат точек
        self.points = []
        self.furniture_points = []

        # Текущая кисть
        self.brush = 'wall'

    def load_images(self):
        """Загрузка изображений"""
        try:
            self.images['net'] = pg.image.load('images/net.png')
        except FileNotFoundError:
            print('Файлы программы не найдены')

        # Считываение файла
        with open('path.txt', 'r', encoding='windows-1251') as file:
            path = file.read()

        if path != '':
            try:
                self.images['background'] = pg.image.load(path)
            except FileNotFoundError:
                self.images['background'] = None
        else:
            self.images['background'] = None
        print(self.images['background'])

    def draw_text(self, surf, text, size, x, y):
        """ Отрисовка текста """
        font = pg.font.Font(pg.font.match_font('Times New Roman'), size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def frame(self):
        """Отрисовка второго окна"""

        #################
        # Логика работы #
        #################

        # Холст
        self.canvas = {
            'can': self.gen_canvas((self.screen.get_size()[0] / 3 * self.multiple,
                                    self.screen.get_size()[1])),
            'rect': pg.Rect(0, 0,
                            self.screen.get_size()[
                                0] / 3 * self.multiple,
                            self.screen.get_size()[1])
        }

        # Отлавливание событий
        for i in pg.event.get():

            # Выход из приложения
            if i.type == pg.QUIT:
                return True

            # Движение мыши по экрану
            if i.type == pg.MOUSEMOTION:
                # Коллизия с ячейками
                for name, square in self.dots.items():
                    if pg.Rect(square[0], square[1], 32.62, 32.62).collidepoint(i.pos):
                        self.dot = (square[0]+32.62/2, square[1]+32.62/2)

            # Нажатие кнопок мыши
            elif i.type == pg.MOUSEBUTTONDOWN:

                # Перебор массива кнопок
                for name in self.buttons:

                    # Коллизия с курсором
                    if self.buttons[name].collidepoint(i.pos):

                        # Вкладки
                        if name == 'pg1':
                            self.pg = True
                        if name == 'pg2':
                            self.pg = False

                        # Очистка
                        if name == 'clear':
                            if self.pg:
                                self.canvas['can'].fill(self.colors['white'])
                                self.points.clear()
                                self.dictionary.clear()
                                self.furniture_points.clear()

                        # Построение по точкам
                        if name == 'dtd':
                            self.brush = 'wall'
                            if self.dot_to_dot:
                                self.dot_to_dot = False
                            else:
                                self.dot_to_dot = True

                        # Кнопка назад
                        if name == 'back':
                            if len(self.last_change) > 0:
                                if self.last_change[-1] == 1:
                                    if len(self.points) > 0:
                                        self.points.pop(-1)
                                if self.last_change[-1] == 0:
                                    if len(self.dictionary) > 0:
                                        self.dictionary.pop(-1)
                                self.last_change.pop(-1)

                        # Сохранение массива точек
                        if name == 'generate':
                            self.save_points1()
                            self.save_points2()
                            return True

                        # Контроль активности кнопок
                        elif name in self.buttons_active.keys() and not self.pg:

                            if self.buttons_active[name]:
                                self.buttons_active[name] = False

                            else:
                                if True not in self.buttons_active.values():
                                    self.buttons_active[name] = True

                        # Иначе сменить кисть
                        elif name not in self.buttons_active.keys():
                            if name in self.names:
                                self.brush = name

                # Запись новых точек в массивы
                if (self.canvas['rect'].collidepoint(i.pos) and not (True in self.buttons_active.values()) or
                        self.pg and self.canvas['rect'].collidepoint(i.pos)):

                    # Запись с учетом dot-to-dot
                    if self.dot_to_dot:
                        self.points.append((self.dot[0] / self.canvas['can'].get_size()[0],
                                            self.dot[1] / self.canvas['can'].get_size()[1],
                                            self.brush))
                        self.last_change.append(1)

                    # Запись без учета dot-to-dot
                    else:
                        self.points.append((i.pos[0] / self.canvas['can'].get_size()[0],
                                            i.pos[1] / self.canvas['can'].get_size()[1],
                                            self.brush))
                        self.brush = 'wall'
                        self.last_change.append(1)

                # Запись положения мебели в словари
                elif self.canvas['rect'].collidepoint(i.pos) and not self.pg:
                    for key in self.buttons_active.keys():
                        if self.buttons_active[key]:
                            self.x, self.y = self.furn_size[key]
                            self.dictionary.append([key,pg.Rect(i.pos[0]-self.x/2, i.pos[1]-self.y/2, self.x , self.y)])
                            self.furniture_points.append((i.pos[0] / self.canvas['can'].get_size()[0],
                                        i.pos[1] / self.canvas['can'].get_size()[1], key))
                            self.last_change.append(0)


        # Перебор массива точек
        for key, val in enumerate(self.points):
            # Отрисовка точек
            pg.draw.circle(
                self.canvas['can'],
                self.colors['black'],
                (val[0] * self.canvas['can'].get_size()[0],
                 val[1] * self.canvas['can'].get_size()[1]),
                3
            )

            # Цвет линии
            line_color = self.colors['black']
            tickness = 2

            if val[2] == 'door':
                line_color = self.colors['green']
                tickness = 2
            elif val[2] == 'window':
                line_color = self.colors['red']
                tickness = 2
            elif val[2] == 'empty':
                tickness = 0
            # Проверка, что точка не одна
            if len(self.points) > 1:
                # Отрисовка линии
                pg.draw.line(
                    self.canvas['can'],
                    line_color,
                    (val[0] * self.canvas['can'].get_size()[0],
                     val[1] * self.canvas['can'].get_size()[1]),
                    (self.points[(key + 1) % len(self.points)][0] *
                     self.canvas['can'].get_size()[0],
                     self.points[(key + 1) % len(self.points)][1] *
                     self.canvas['can'].get_size()[1]),
                    tickness
                )

        #######################
        # Отрисовка элементов #
        #######################

        # Заполнение экрана черным
        self.screen.fill((30,30,30))

        # Отрисовка холста
        self.screen.blit(self.canvas['can'],
                         self.canvas['rect'])
        if self.pg:
            pg.draw.rect(self.screen, 'yellow', self.buttons['pg1'], 4)
            pg.draw.rect(self.screen, 'white', self.buttons['pg2'], 4)
        else:
            pg.draw.rect(self.screen, 'yellow', self.buttons['pg2'], 4)
            pg.draw.rect(self.screen, 'white', self.buttons['pg1'], 4)

        if self.dot_to_dot:
            pg.draw.rect(self.screen, 'yellow', self.buttons['dtd'], 0)
            pg.draw.circle(self.screen, 'red', self.dot, 4)
        else:
            pg.draw.rect(self.screen, 'pink', self.buttons['dtd'], 0)

        pg.draw.rect(self.screen, 'orange', self.buttons['generate'], 4)
        pg.draw.rect(self.screen, 'gray', self.buttons['back'], 0)

        # Заполнение словаря точек
        k = 0
        y = 7
        for i in range(22):
            x = 6
            for j in range(21):
                self.dots[str(k+1)] = (x-32.62/2, y-32.62/2)
                x += 32.62
                k += 1
            y += 32.62



        self.screen.blit(self.back, (1092, 454))
        self.screen.blit(self.ddd, (1092, 352))

        # Текст
        Main.draw_text(self, self.screen, '––>', 60, self.width - 170, 605)
        Main.draw_text(self, self.screen, 'Back', 40, self.width - 175, 465)
        Main.draw_text(self, self.screen, 'Dot-to-dot', 40, self.width - 125, 365)
        Main.draw_text(self, self.screen, 'Furniture', 40, self.width - 175, 65)
        Main.draw_text(self, self.screen, 'Instruments', 40, self.width - 175, 165)

        pg.draw.rect(self.screen, 'white', pg.Rect(1090, 350, 70, 70), 4)
        pg.draw.rect(self.screen, 'white', pg.Rect(1090, 450, 70, 70), 4)

        # Элементы на первой вкладке
        if self.pg:
            # Кнопки
            pg.draw.rect(self.screen, 'white', self.buttons['clear'], 0)
            pg.draw.rect(self.screen, 'green', self.buttons['door'], 0)
            pg.draw.rect(self.screen, self.colors['not_hovered'], self.buttons['wall'], 0)
            pg.draw.rect(self.screen, 'red', self.buttons['window'], 0)
            pg.draw.rect(self.screen, self.colors['hovered'], self.buttons['empty'], 0)

            # Изображения
            self.screen.blit(self.clear, (680, 10))
            self.screen.blit(self.wall, (690, 150))
            self.screen.blit(self.window, (685, 295))
            self.screen.blit(self.door, (690, 450))
            self.screen.blit(self.empty, (692, 602))

            self.n = 20
            for square in range(5):
                pg.draw.rect(self.screen, 'white', pg.Rect(690, self.n, 70, 70), 4)
                if square < 1:
                    self.n += 130
                else:
                    self.n += 150

            # Активность кнопок стен
            if self.brush in self.names:
                pg.draw.rect(self.screen, 'yellow', self.buttons[self.brush], 4)
            else:
                pg.draw.rect(self.screen, 'yellow', self.buttons['wall'], 4)

            # Текст
            Main.draw_text(self, self.screen, 'Clear all', 40, self.width - 525, 33)
            Main.draw_text(self, self.screen, 'Wall', 40, self.width - 525, 165)
            Main.draw_text(self, self.screen, 'Window', 40, self.width - 525, 315)
            Main.draw_text(self, self.screen, 'Door', 40, self.width - 525, 463)
            Main.draw_text(self, self.screen, 'Empty', 40, self.width - 525, 615)




        # Элементы на второй вкладке
        else:
            # Текст
            Main.draw_text(self, self.screen, 'Chair', 40, self.width - 525, 33)
            Main.draw_text(self, self.screen, 'Table', 40, self.width - 525, 165)
            Main.draw_text(self, self.screen, 'Nightstand', 40, self.width - 525, 315)
            Main.draw_text(self, self.screen, 'Bed', 40, self.width - 525, 463)
            Main.draw_text(self, self.screen, 'Closet', 40, self.width - 525, 613)



            # Кнопки и их активность
            for name in self.buttons:
                if name in self.buttons_active.keys():
                    if self.buttons_active[name]:
                        pg.draw.rect(self.screen, 'yellow', self.buttons[name], 0)
                    else:
                        pg.draw.rect(self.screen, 'pink', self.buttons[name], 0)

            # Мебель на холсте
            for rect, active in self.buttons_active.items():
                if active and not self.pg:
                    self.x, self.y = self.furn_size[rect]
                    pg.draw.rect(self.screen, self.furn_colors[rect],
                                 pg.Rect(pg.mouse.get_pos()[0]-self.x/2, pg.mouse.get_pos()[1]-self.y/2,
                                         self.x, self.y), 3)

            self.screen.blit(self.chair, (688, 19))
            self.screen.blit(self.table, (691.5, 143))
            self.screen.blit(self.night, (692, 303))
            self.screen.blit(self.bed, (677, 435))
            self.screen.blit(self.closet, (695, 605))

            self.n = 20
            for square in range(5):
                pg.draw.rect(self.screen, 'white', pg.Rect(690, self.n, 70, 70), 4)
                if square < 1:
                    self.n += 130
                else:
                    self.n += 150


        # Мебель на холсте
        for name, rect in self.dictionary:
            pg.draw.rect(self.screen, self.furn_colors[name], rect)

        # Разделительная линия
        pg.draw.rect(self.screen, 'white', pg.Rect(self.width-350, 0, 2, 700))

        # Отрисовка
        pg.display.update()

        # Тик таймера на fps
        self.clock.tick(self.fps)

        return False

    def gen_button(self, size, text):
        """Генерация красивой кнопки"""

        # Поверхность кнопки
        surf = pg.Surface(size)

        # Изображение
        image = pg.transform.scale(self.images[text],
                                   (int(size[0]), int(size[1])))

        # Фоновая картинка
        surf.blit(image, image.get_rect())

        return surf


    def gen_canvas(self, size):
        """Генерация холста"""

        # Поверхность
        surf = pg.Surface(size)

        # Заливка белым
        surf.fill(self.colors['white'])

        # Отрисовка фонового изображения
        if self.images['background'] is None:
            surf.blit(self.images['net'], self.images['net'].get_rect())
        else:
            img = self.images['background']
            img = pg.transform.scale(img, (int(size[0]), int(size[1])))
            img.set_alpha(128)
            surf.blit(img, img.get_rect())

        # Обводка
        pg.draw.rect(surf, self.colors['black'], (1, 1, size[0] - 1, size[1] - 2), 1)

        return surf



    def save_points1(self):
        """Сохранение точек в csv формате"""
        # Открытие файла
        with open('point.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, lineterminator='\n')
            # Запись массива
            writer.writerows(self.points)

    def save_points2(self):
        """Сохранение точек в csv формате"""
        # Открытие файла
        with open('furniture.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, lineterminator='\n')
            # Запись массива
            writer.writerows(self.furniture_points)


if __name__ == '__main__':
    main = Main()
    while not main.frame():
        pass
