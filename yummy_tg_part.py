from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from yummy_sql_part import get_random
from yummy_telegraph_part import create_page
import os


bot = Bot(token=os.getenv('TOKEN_1'))
dp = Dispatcher(bot)


random_button = KeyboardButton("🎲 Случайное аниме 🎲")
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(random_button)


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(
                            message.from_user.id,
                            'Нажмите на кнопку "Случайное аниме", чтобы получить случайную рекомендацию',
                            reply_markup=keyboard_menu
    )

@dp.message_handler()
async def process_message(message: types.Message):
    if message.text == '🎲 Случайное аниме 🎲':
        try:
            anime_data = get_random()
            url_button = types.InlineKeyboardButton('Смотреть на YummyAnime', url=anime_data['url'])
            keyboard_markup = types.InlineKeyboardMarkup().add(url_button)

            try:
                page_url = await create_page(anime_data["name"], anime_data["description"])
            except Exception as ex:
                page_url = False
                print(ex)

            await bot.send_photo(
                                chat_id=message.from_user.id,
                                photo=anime_data['poster_url'],
                                caption=

                                        f'<b>{anime_data["name"]}</b>\n'
                                        f'\n'
                                        f'Рейтинг: {anime_data["rate"]}\n'
                                        f'Статус: {anime_data["status"]}\n'
                                        f'Год: {anime_data["year"]}\n'
                                        f'Жанры: {anime_data["category"]}\n'
                                        f'Тип: {anime_data["type"]}\n'
                                        f'\n'
                                        f'<a href="{page_url}">{"Нажмите, чтобы прочесть описание" if page_url else "Описание временно недоступно."}</a>',

                                reply_markup=keyboard_markup,
                                parse_mode=types.ParseMode.HTML
            )
        except Exception as ex:
            print(ex)
            await bot.send_message(message.from_user.id, 'Произошла ошибка. Попытайтесь ещё раз!')
    else:
        await message.reply('Обратитесь к команде /start, чтобы получить случайную рекомендацию')


executor.start_polling(dp, skip_updates=True)
