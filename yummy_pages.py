# import asyncio

from aiograph import Telegraph

# loop = asyncio.get_event_loop()
telegraph = Telegraph()

async def create_page(name, description):
    await telegraph.create_account('YummyBot')
    page = await telegraph.create_page(name,
                                       f'<b><i>Обратите внимание, является ли данное аниме первым в цикле на просмотр. В противном случае возмножно наткнуться на спойлеры.\n</i></b>'
                                       f'\n'
                                       f'{description.strip() if description else "Описание отсутствует."}', author_name='YummyAnime', author_url='https://yummyanime.club')


    # print(page.url)
    return page.url


# if __name__ == '__main__':
#     try:
#         loop.run_until_complete(create_page('a', 'b'))
#     except (KeyboardInterrupt, SystemExit):
#         pass
#     finally:
#         loop.run_until_complete(telegraph.close())  # Close the aiohttp.ClientSession