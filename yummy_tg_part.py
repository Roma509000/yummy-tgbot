from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, request
from yummy_sql_part import get_random
from yummy_telegraph_part import create_page
import os
import asyncio

TOKEN = '5283101641:AAHp9tQBjmlmIjFjZlnja3OVvBjptO3Q-aU'
APP_URL = f'https://yummy-tgbot.herokuapp.com/{TOKEN}'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
server = Flask(__name__)

button_random = KeyboardButton("🎲 Случайное аниме 🎲")
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_random)


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(
                            message.from_user.id,
                            'Нажмите на кнопку "Случайное аниме", чтобы получить случайную рекомендацию',
                            reply_markup=keyboard_menu
    )

@dp.message_handler()
async def randomize(message: types.Message):
    if message.text == '🎲 Случайное аниме 🎲':
        try:
            anime_data = get_random()
            url_button = types.InlineKeyboardButton('Смотреть на YummyAnime', url=anime_data['url'])
            keyboard_markup = types.InlineKeyboardMarkup().add(url_button)

            await bot.send_photo(message.from_user.id, anime_data['poster_url'],
                                 f'<b>{anime_data["name"]}</b>\n'
                                 f'\n'
                                 f'Рейтинг: {anime_data["rate"]}\n'
                                 f'Статус: {anime_data["status"]}\n'
                                 f'Год: {anime_data["year"]}\n'
                                 f'Жанры: {anime_data["category"]}\n'
                                 f'Тип: {anime_data["type"]}\n'
                                 f'\n'
                                 f'<a href="{create_page(anime_data["name"], anime_data["description"])}">Нажмите, чтобы прочесть описание</a>',
                                 reply_markup=keyboard_markup,
                                 parse_mode=types.ParseMode.HTML)
        except Exception as ex:
            print(ex)
            await bot.send_message(message.from_user.id, 'Произошла ошибка. Попытайтесь ещё раз!')
    else:
        await message.reply('Обратитесь к команде /start, чтобы получить случайную рекомендацию')


@server.route('/' + TOKEN, methods=['POST'])
async def get_message():
    json_str = request.get_json().decode('utf-8')
    update = types.Update.as_json(json_str)
    await bot.get_updates(allowed_updates=[update])


@server.route('/')
async def webhook():
    await bot.delete_webhook()
    await bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=os.getenv('PORT', 5000))