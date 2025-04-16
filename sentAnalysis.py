import pickle
import re

from pymorphy2 import MorphAnalyzer

modelLRname = 'models/finalized_model.sav'
modelIDFname = 'models/TfIdfVectorizer.pk'
model_lr_lemm = pickle.load(open(modelLRname, 'rb'))
count_idf_lemm = pickle.load(open(modelIDFname, 'rb'))
stopwords_ru = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его',
                'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от',
                'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже',
                'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом',
                'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их',
                'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж',
                'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один',
                'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно',
                'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас',
                'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою',
                'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда',
                'конечно', 'всю', 'между']
patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
morph = MorphAnalyzer()


def text_preparation(doc):
    doc = re.sub(patterns, ' ', doc)
    doc = [word for word in doc.split() if word not in stopwords_ru]
    doc = " ".join(doc)

    tokens = []
    for token in doc.split():
        token = token.strip()
        token = morph.normal_forms(token)[0]
        tokens.append(token)

    lemm_sample = ' '.join(tokens).split('br')

    return lemm_sample


def predict_tonality(text):
    lemm_sample = text_preparation(text)

    feedback_idf = count_idf_lemm.transform(lemm_sample)

    feedback_negative_proba = model_lr_lemm.predict_proba(feedback_idf)

    if feedback_negative_proba[0, 0] > 0.55:
        class_feedback = "негативный"
    elif feedback_negative_proba[0, 0] < 0.45:
        class_feedback = "позитивный"
    else:
        class_feedback = "нейтральный"

    result = class_feedback

    return result
