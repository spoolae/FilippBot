import json
import random
from fuzzywuzzy import fuzz
from message_handler_functions import fuzzy_match

def load_responses(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def handle_message(message_text):
    responses = load_responses('responses.json')
    message_text_lower = message_text.lower()

    # Инициализация переменной response_type
    response_type = "text"

    # Список для хранения всех совпадений
    all_matches = []

    for keyword, response_data in responses.items():
        keyword_list = [kw.lower() for kw in keyword.split(', ')]
        for kw in keyword_list:
            if kw in message_text_lower:
                response_type = random.choices(["text", "sticker"], [len(response_data.get("text", [])), len(response_data.get("sticker", []))])[0]
                response_list = response_data.get(response_type, [])
                if response_list:
                    response = random.choice(response_list)
                    return response, response_type == "sticker"

        # Если ключевое слово не найдено, добавляем ближайшее совпадение в список
        closest_match = fuzzy_match(message_text_lower, keyword_list)
        if closest_match is not None:
            all_matches.append((closest_match, response_data))

    # Если есть ближайшие совпадения, выберите случайный ответ из них
    if all_matches:
        closest_match, response_data = random.choice(all_matches)
        response_type = random.choices(["text", "sticker"], [len(response_data.get("text", [])), len(response_data.get("sticker", []))])[0]
        response_list = response_data.get(response_type, [])
        if response_list:
            response = random.choice(response_list)
            return response, response_type == "sticker"

    # Если ни ключевое слово, ни ближайшее совпадение не найдены
    # Выберите ответ другого типа

    default_responses = responses.get("default_responses", {})
    response_type = random.choices(["text", "sticker"], [len(default_responses.get("text", [])), len(default_responses.get("sticker", []))])[0]
    response_list = default_responses.get(response_type, [])
    if response_list:
        response = random.choice(response_list)
        return response, response_type == "sticker"

    # Если даже другой тип ответа отсутствует, вернуть пустую строку
    return "Сори, я сломался...", False
