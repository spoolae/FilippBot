import random
from fuzzywuzzy import fuzz

def fuzzy_match(word, word_list):
    max_similarity = 0
    best_match = None

    for candidate in word_list:
        similarity = fuzz.ratio(word, candidate)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = candidate

    # Уменьшаем порог сходства для более широкого поиска
    your_threshold = 65  # Уменьшенный порог сходства
    if max_similarity >= your_threshold:
        return best_match
    return None

def add_lowercase_start(text):
    # Добавление случайного начала сообщения с маленькой буквы с вероятностью 10%
    if random.random() < 0.1:
        text = text.lower()
    return text

def add_random_error(text):
    # Добавление случайной ошибки в слове с вероятностью 2.5%
    if random.random() < 0.025:
        random_index = random.randint(0, len(text) - 1)
        random_char = random.choice('абвгдежзийклмнопрстуфхцчшщъьэюя')
        text = text[:random_index] + random_char + text[random_index + 1:]
    return text
