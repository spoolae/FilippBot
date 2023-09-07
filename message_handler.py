import json
import random
from fuzzywuzzy import fuzz

def load_responses(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def fuzzy_match(word, word_list):
    max_similarity = 0
    best_match = None

    for candidate in word_list:
        similarity = fuzz.ratio(word, candidate)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = candidate

    # Уменьшаем порог сходства для более широкого поиска
    your_threshold = 70  # Уменьшенный порог сходства
    if max_similarity >= your_threshold:
        return best_match
    return None

def handle_message(message_text):
    responses = load_responses('responses.json')
    message_text_lower = message_text.lower()

    # Список для хранения всех совпадений
    all_matches = []

    for keyword, response_list in responses.items():
        keyword_list = [kw.lower() for kw in keyword.split(', ')]
        for kw in keyword_list:
            if kw in message_text_lower:
                response = random.choice(response_list)
                response = add_lowercase_start(response)
                response = add_random_error(response)
                return response

        # Если ключевое слово не найдено, добавляем ближайшее совпадение в список
        closest_match = fuzzy_match(message_text_lower, keyword_list)
        if closest_match is not None:
            all_matches.append((closest_match, response_list))

    # Если есть ближайшие совпадения, выберите случайный ответ из них
    if all_matches:
        closest_match, response_list = random.choice(all_matches)
        response = random.choice(response_list)
        response = add_lowercase_start(response)
        response = add_random_error(response)
        return response

    # Если ни ключевое слово, ни ближайшее совпадение не найдены, вернуть случайное сообщение
    default_response = random.choice(responses['default_responses'])
    default_response = add_lowercase_start(default_response)
    default_response = add_random_error(default_response)

    return default_response

def add_lowercase_start(text):
    # Добавление случайного начала сообщения с маленькой буквы с вероятностью 10%
    if random.random() < 0.1:
        text = text.lower()
    return text

def add_random_error(text):
    # Добавление случайной ошибки в слове с вероятностью 7.5%
    if random.random() < 0.075:
        random_index = random.randint(0, len(text) - 1)
        random_char = random.choice('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        text = text[:random_index] + random_char + text[random_index + 1:]
    return text
