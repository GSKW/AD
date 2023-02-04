import pymorphy2
import re


class Adjectives:
    def __init__(self):
        pass

    def adj_check(self, word):
        morph = pymorphy2.MorphAnalyzer(lang='ru')
        word = morph.parse(word)[0]
        return ('ADJF' in word.tag)

    def splitting(self, string):
        string_arr = re.findall('[a-zа-яё]+', string, flags=re.IGNORECASE)
        return string_arr

    def get_agj(self, string):
        adj_list = []
        string_arr = self.splitting(string)
        for word in string_arr:
            if self.adj_check(word):
                adj_list.append(word.lower())
        return adj_list