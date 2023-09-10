import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from config import TELEGRAM_TOKEN
from user_data_manager import UserDataManager
from message_handler import handle_message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
user_data_manager = UserDataManager()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_data_manager.handle_start_command(user_id, message.from_user)

    await message.reply("Welcome!\nYour data has been saved.")

@dp.message_handler(commands=['info'])
async def get_user_info(message: types.Message):
    user_id = message.from_user.id
    info_message = user_data_manager.get_user_info(user_id)
    
    await message.reply(info_message)

@dp.message_handler()
async def process_message(message: types.Message):
    response, is_sticker = handle_message(message.text)
    
    if is_sticker:
        random_delay = random.uniform(0.5, 3.0)
        await bot.send_chat_action(message.chat.id, "choose_sticker")
        await asyncio.sleep(random_delay)
        await message.reply_sticker(response)

    else:
        await bot.send_chat_action(message.chat.id, "typing")
        message_length = len(message.text)
        delay_seconds = 0.5 + (0.1 * message_length)
        random_delay = random.uniform(delay_seconds - 0.1, delay_seconds + 0.1)
        await asyncio.sleep(random_delay)
        await message.reply(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
