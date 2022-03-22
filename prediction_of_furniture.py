import fasttext
import numpy as np
import subprocess
from draw_bar import get_path




# Модели
small_model_wiki = 'ccru.300.bin'
small_model_twitter = 'twitter.100.bin'
small_model_wiki_lenta = 'wiki_lenta.300.bin'

# Основные слова спецификации
word1 = ['современный', 'актуальный', 'новый']
word2 = ['старый', 'древний']
word3 = ['стандартный']

# Данные для проверки
valid_data = {
    'уютный':2,
  'стильный':1,
  'обычная':3,
  'современная':1,
  'старинная':2,
  'новый':1,
  'теплая':2,
  'холодная':1,
  'простая':3,
  'классическая':3,
  'дешевая':3,
}

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

class Classifier:
    """ Нейросеть """
    def __init__(self, model_name=small_model_wiki):
        """ Инициализация """
        subprocess.Popen(["python", get_path()])

        print("Loading model...")

        self.model = fasttext.FastText.load_model(model_name)
        self.models_embs = []
        self.size = self.model.get_dimension()
        self.models_embs.append(self.get_emb_mod_vecs(word1))
        self.models_embs.append(self.get_emb_mod_vecs(word2))
        self.models_embs.append(self.get_emb_mod_vecs(word3))
    
    def get_emb_mod_mean(self, words):
        """ Усредненные эмбединги """
        vecs = np.empty((0, self.size))
        mean_vecs = np.empty((self.size))
        for word in words:
            word_vec = self.model[word]
            word_vec = word_vec[np.newaxis, :]
            vecs = np.concatenate([vecs, word_vec], axis=0)
        for column in range(self.size):
            mean_vecs[column] = np.mean(vecs[:, column])
        return mean_vecs

    def get_emb_mod_vecs(self, words):
        """ Эмбединги """
        vecs = np.empty((0, self.size))
        for word in words:
            word_vec = self.model[word]
            word_vec = word_vec[np.newaxis, :]
            vecs = np.concatenate([vecs, word_vec], axis=0)
        return vecs

    def calculate_dot_simil(self, vec1, vec2):
        """ Расчет схожести """
        w = []
        for i in range(self.size):
            w.append(vec1[i] * vec2[i])
        return sum(w)

    def get_vect_norm(self, vec):
        """ Норма векторов """
        return np.sqrt(np.sum(np.power(vec, 2)))

    def calculate_cosine_simil(self, vec1, vec2):
        """
        Расчет схожести через косинусное расстояние
        """
        return self.calculate_dot_simil(vec1, vec2)/\
               (self.get_vect_norm(vec1)*self.get_vect_norm(vec2))

    def predict_model(self, our_words):
        """ Предсказывание модели """
        model2max_sim = self.predict_probs(our_words)
        max_model, max_model_sim = 1, model2max_sim[1]
        for key, val in model2max_sim.items():
            if val > max_model_sim:
                max_model_sim = val
                max_model = key
        # print(get_key(model2max_sim, max(model2max_sim.values())))
        return max_model

    def calc_accuracy(self, data):
        """ Метрика """
        score, len_words = 0, len(data)
        for word, true_model in data.items():
            if true_model == self.predict_model(word):
                score += 1
        return score/len_words

    def predict_probs(self, our_words):
        """  """
        our_vec = self.get_emb_mod_mean(our_words)
        model2sim, model2max_sim = {}, {}
        for model_index in range(len(self.models_embs)):
            model2sim[model_index] = []
            for word in self.models_embs[model_index]:
                model2sim[model_index].append(self.calculate_cosine_simil(word, our_vec))
        for model, sim_list in model2sim.items():
            model2max_sim[model + 1] = max(sim_list)
        return model2max_sim

    def predict_sorted_models(self, our_words):
        """  """
        model2max_sim = self.predict_probs(our_words)
        sorted_models_probs = sorted(model2max_sim.items(), key = lambda x: x[1], reverse=True)
        sorted_models = []
        for array in sorted_models_probs:
            sorted_models.append(array[0])
        return sorted_models

if __name__ == '__main__':
    classifier_wiki = Classifier(small_model_wiki)
# classifier_twitter = Classifier(small_model_twitter)
# classifier_wiki_lenta = Classifier(small_model_wiki_lenta)
# print(calc_accuracy(valid_data, predict_model))
#
# #Ввод:
# print(classifier_wiki.predict_probs(['уютный']))
# print(classifier_wiki.predict_sorted_models(['уютный']))
# print(classifier_wiki.calc_accuracy(valid_data))
# print('-'*8)
# print(classifier_twitter.predict_model(['уютный']))
# print(classifier_twitter.calc_accuracy(valid_data))
# print('-'*8)
# print(classifier_wiki_lenta.predict_model(['уютный']))
# print(classifier_wiki_lenta.calc_accuracy(valid_data))
# #Вывод:
#1 цифра, означающая в каком из стилей делать дизайн
