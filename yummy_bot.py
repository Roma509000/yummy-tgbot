'''**************************************************SQL PART**************************************************'''
import sqlite3
# from pprint import pprint


def get_random():
    connection = sqlite3.connect('yummy_data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM yummy ORDER BY random() LIMIT 1')

    dict_of_data = {}
    unorganised_data = cursor.fetchone()
    keys = ['name', 'rate', 'status', 'year', 'category', 'type', 'description', 'url', 'poster_url']
    for key, data in zip(keys, unorganised_data):
        dict_of_data[key] = data

    # pprint(dict_of_data)

    connection.close()

    return dict_of_data


'''**************************************************TELEGRAM PART**************************************************'''
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
from yummy_pages import create_page


bot = Bot(token="5283101641:AAFHLqoynQNswFdIFFbHcE-Sct_uWhAYEIU")
dp = Dispatcher(bot)

button_random = KeyboardButton("🎲 Случайное аниме 🎲")
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_random)


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Нажмите на кнопку "Случайное аниме", чтобы получить случайную рекомендацию',
                           reply_markup=keyboard_menu)

@dp.message_handler()
async def randomize(message: types.Message):
    if message.text == '🎲 Случайное аниме 🎲':
        try:
            anime_data = get_random()
            press_btn = types.InlineKeyboardButton('Смотреть на YummyAnime', url=anime_data['url'])
            keyboard_markup = types.InlineKeyboardMarkup().add(press_btn)
            await bot.send_photo(message.from_user.id, anime_data['poster_url'],
                                 f'<b>{anime_data["name"]}</b>\n'
                                 f'\n'
                                 f'Рейтинг: {anime_data["rate"]}\n'
                                 f'Статус: {anime_data["status"]}\n'
                                 f'Год: {anime_data["year"]}\n'
                                 f'Жанры: {anime_data["category"]}\n'
                                 f'Тип: {anime_data["type"]}\n'
                                 f'\n'
                                 f'<a href="{await create_page(anime_data["name"], "https://www.youtube.com")}">Нажмите, чтобы прочесть описание</a>',
                                 reply_markup=keyboard_markup,
                                 parse_mode=types.ParseMode.HTML)
        except Exception as ex:
            print(ex)
            await bot.send_message(message.from_user.id, 'Произошла ошибка. Попытайтесь ещё раз!')
    else:
        await message.reply('Обратитесь к команде /start, чтобы получить случайную рекомендацию')


executor.start_polling(dp, skip_updates=True)
