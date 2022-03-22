""" Модуль фронтенда 1 """

import pygame as pg
import csv

tk = False

class Main:
    """ Главный класс приложения """

    def __init__(self):
        """ Инициализация переменных """

        # Инициализация Pygame
        pg.init()

        # Рамки
        self.height = 1000
        self.width = 700
        self.thickness = 2


        # Особые цвета
        self.colors = {
            'not_hovered': 'dodgerblue2',
            'hovered': 'lightskyblue3',
        }

        # FPS
        self.clock = pg.time.Clock()
        self.fps = 30

        # Кнопки
        self.buttons = {
            # Главные кнопки
             'btn_add': pg.Rect(225, 590, 250, 75),
            'btn_skip': pg.Rect(750, 600, 200, 50),

            # Побочные кнопки
             '1': pg.Rect(20, 120, 200, 50),    '2': pg.Rect(270, 120, 200, 50),
             '3': pg.Rect(520, 120, 200, 50),   '4': pg.Rect(770, 120, 200, 50),
             '5': pg.Rect(20, 240, 200, 50),    '6': pg.Rect(270, 240, 200, 50),
             '7': pg.Rect(520, 240, 200, 50),   '8': pg.Rect(770, 240, 200, 50),

             '9': pg.Rect(20, 360, 200, 50),   '10': pg.Rect(270, 360, 200, 50),
            '11': pg.Rect(520, 360, 200, 50),  '12': pg.Rect(770, 360, 200, 50),
            '13': pg.Rect(20, 480, 200, 50),   '14': pg.Rect(270, 480, 200, 50),
            '15': pg.Rect(520, 480, 200, 50),  '16': pg.Rect(770, 480, 200, 50),
        }

        # Линии
        self.lines = [
            # Вертикальные
            pg.Rect(700, 550, self.thickness, 150),
            # Горизонтальные
            pg.Rect(0, 100, self.height, self.thickness),
            pg.Rect(0, 550, self.height, self.thickness),
        ]

        # Размеры окна
        self.screen = pg.display.set_mode((self.height, self.width))
        self.screen.fill((30, 30, 30))


        # Начальные координаты слов
        self.word_start_pos_x = 120
        self.word_start_pos_y = 130

        # Списки слов
        self.words_index = set()
        self.words = {
             '1': 'современная',   '2':'старинная',    '3':'просторная',  '4':'большая',
             '5': 'классическая',  '6':'простая',      '7':'стильная',    '8':'теплая',
             '9': 'уютная',       '10':'компактная',  '11':'детская',    '12':'холодная',
            '13': 'светлая',      '14':'тёмная',      '15':'обычная',    '16':'жаркая'
        }

        # Конечный список слов
        self.words_list = []

    def draw_button(self, button, color, width):
        """ Отрисовка кнопок """
        pg.draw.rect(self.screen, color, button, width)

    def draw_frames(self, color, width):
        """ Отрисовка линий-декораций """
        for line in self.lines:
            pg.draw.rect(self.screen, color, line, width)

    def draw_text(self, surf, text, size, x, y):
        """ Отрисовка текста """
        font = pg.font.Font(pg.font.match_font('Times New Roman'), size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def save_words(self, path):
        """ Сохранение выбранных слов в файл """
        pass

    def draw_all(self):

        for word in self.words:
            if self.word_start_pos_y > 600:
                break
            self.draw_text(self.screen, self.words[word], 30, self.word_start_pos_x, self.word_start_pos_y)
            self.word_start_pos_x += 250
            if self.word_start_pos_x > 950:
                self.word_start_pos_x = 120
                self.word_start_pos_y += 120

        for name, btn in self.buttons.items():
            if name in self.words_index:
                pg.draw.rect(self.screen, self.colors['hovered'], self.buttons[name], 2)
            else:
                pg.draw.rect(self.screen, self.colors['not_hovered'], self.buttons[name], 2)

    def frame(self):
        """ Основная функция """

        self.draw_all()

        # Рамки и линии
        self.draw_frames('white', 0)

        # Текст
        self.draw_text(self.screen, 'Auto Design Project', 50, 225, 25)
        self.draw_text(self.screen, 'Ваша квартира...', 45, 825, 50)
        self.draw_text(self.screen, 'Пропустить', 30, 850, 610)
        self.draw_text(self.screen, '––>', 80, 350, 587)

                           ########################
       ##################### ОТЛАВЛИВАНИЕ СОБЫТИЙ ######################
                           ########################

        for event in pg.event.get():

            # CОБЫТИЕ: Выход из приложения
            if event.type == pg.QUIT:
                return True

                # СОБЫТИЕ: Нажатие кнопки мыши
            if event.type == pg.MOUSEBUTTONDOWN:

                # Итерация по кнопкам
                for name in self.buttons:

                    # Коллизия с кнопкой
                    if self.buttons[name].collidepoint(event.pos):

                        # Работа кнопки Далее
                        if self.buttons[name] == self.buttons['btn_add']:
                            for index in self.words_index:
                                self.words_list.append(self.words[index])

                            # Запись в файл
                            with open('words.csv', 'w', encoding='UTF-8') as file:
                                writer = csv.writer(file)
                                writer.writerows([self.words_list])
                            return True

                        # Работа кнопки Skip
                        elif self.buttons[name] == self.buttons['btn_skip']:
                            return True

                        # Проверка слова на наличие в множестве
                        else:
                            if name in self.words_index:
                                self.words_index.remove(name)
                            else:
                                self.words_index.add(name)

                # СОБЫТИЕ: Движение мыши
            if event.type == pg.MOUSEMOTION:
                for name in self.buttons:
                    if self.buttons[name].collidepoint(event.pos):
                        self.draw_button(self.buttons[name], self.colors['hovered'], self.thickness)

                # Отрисовка кадра
            pg.display.flip()
            self.clock.tick(self.fps)




if __name__ == '__main__':
    main = Main()
    while not main.frame():
        pass
