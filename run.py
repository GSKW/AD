"""Модуль запуска"""

import csv
import subprocess


#
#pip
#

import window1new
import window2new
import window3new

import prediction_of_furniture


def main():
    """ Главная функция """

    # Нулевое окно
    win0 = window3new.Main()
    win0.frame()
    while not win0.frame():
        pass


    # # Первое окно
    win1 = window1new.Main()
    win1.frame()
    classifier = prediction_of_furniture.Classifier()
    while not win1.frame():
        pass

    # Второе окно
    win2 = window2new.Main()
    while not win2.frame():
        pass

    words = []
    with open('words.csv', 'r', encoding='windows-1251') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row)
    words = words[0]

    sorted_models = classifier.predict_sorted_models(words)
    with open('models.csv', 'w', encoding='utf-8') as file:
        file.write(','.join([str(model) for model in sorted_models]))

    subprocess.run(['open', '-n', '../bin2.app'])


if __name__ == '__main__':
    main()
