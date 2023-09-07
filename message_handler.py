import json
import random
import difflib

def load_responses(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_closest_match(word, word_list):
    if len(word) >= 10:
        cutoff = 0.1
    elif len(word) >= 5:
        cutoff = 0.2
    else:
        cutoff = 0.8

    matches = difflib.get_close_matches(word, word_list, cutoff=cutoff)
    if matches:
        return matches[0]
    return None

def handle_message(message_text):
    responses = load_responses('responses.json')
    message_text_lower = message_text.lower()

    for keyword, response_list in responses.items():
        keyword_list = [kw.lower() for kw in keyword.split(', ')]
        for kw in keyword_list:
            if kw in message_text_lower:
                response = random.choice(response_list)
                response = add_lowercase_start(response)
                response = add_random_error(response)
                return response

    # Если ключевое слово не найдено, попробуйте найти ближайшее совпадение
    for keyword, response_list in responses.items():
        closest_match = get_closest_match(message_text_lower, keyword_list)
        if closest_match is not None:
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
    # Добавление случайной ошибки в слове с вероятностью 15%
    if random.random() < 0.15:
        random_index = random.randint(0, len(text) - 1)
        random_char = random.choice('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        text = text[:random_index] + random_char + text[random_index + 1:]
    return text
