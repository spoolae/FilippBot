import json
import random
from fuzzywuzzy import fuzz
from message_handler_functions import fuzzy_match, add_lowercase_start, add_random_error

def load_responses(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def handle_message(message_text):
    responses = load_responses('responses.json')
    message_text_lower = message_text.lower()

    # Список для хранения всех совпадений
    all_matches = []

    for keyword, response_data in responses.items():
        keyword_list = [kw.lower() for kw in keyword.split(', ')]
        for kw in keyword_list:
            if kw in message_text_lower:
                response_type = random.choice(["text", "sticker"])
                response_list = response_data[response_type]
                response = random.choice(response_list)
                response = add_lowercase_start(response)
                response = add_random_error(response)
                return response, response_type == "sticker"

        # Если ключевое слово не найдено, добавляем ближайшее совпадение в список
        closest_match = fuzzy_match(message_text_lower, keyword_list)
        if closest_match is not None:
            all_matches.append((closest_match, response_data))

    # Если есть ближайшие совпадения, выберите случайный ответ из них
    if all_matches:
        closest_match, response_data = random.choice(all_matches)
        response_type = random.choice(["text", "sticker"])
        response_list = response_data[response_type]
        response = random.choice(response_list)
        response = add_lowercase_start(response)
        response = add_random_error(response)
        return response, response_type == "sticker"

    # Если ни ключевое слово, ни ближайшее совпадение не найдены, вернуть случайное сообщение
    default_response_data = responses['default_responses']
    response_type = random.choice(["text", "sticker"])
    response_list = default_response_data[response_type]
    response = random.choice(response_list)
    response = add_lowercase_start(response)
    response = add_random_error(response)

    return response, response_type == "sticker"
