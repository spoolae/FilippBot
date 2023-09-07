import json

class UserDataManager:
    def __init__(self):
        self.users_data = {}
        self.load_users_data()

    def load_users_data(self):
        try:
            with open('users_data.json', 'r', encoding='utf-8') as file:
                self.users_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users_data = {}

    def save_users_data(self):
        with open('users_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.users_data, file, ensure_ascii=False, indent=4)

    def handle_start_command(self, user_id, user_data):
        if user_id not in self.users_data:
            self.users_data[user_id] = {}
            self.users_data[user_id]['Username'] = user_data.username
            self.users_data[user_id]['First Name'] = user_data.first_name
            self.users_data[user_id]['Last Name'] = user_data.last_name
            self.save_users_data()

    def get_user_info(self, user_id):
        if user_id in self.users_data:
            user_info = self.users_data[user_id]
            info_message = "User Info:\n"
            info_message += f"Username: {user_info.get('Username', 'N/A')}\n"
            info_message += f"First Name: {user_info.get('First Name', 'N/A')}\n"
            info_message += f"Last Name: {user_info.get('Last Name', 'N/A')}\n"
            return info_message
        else:
            return "User data not found."