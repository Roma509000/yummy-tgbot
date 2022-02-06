from telegraph.aio import Telegraph
import os


async def create_page(name, description):
    telegraph = Telegraph(access_token=os.getenv('TOKEN_2'))
    account = await telegraph.get_account_info()

    page = await telegraph.create_page(
        title=name,
        html_content=f'''
                            <b><i>Обратите внимание, является ли данное аниме первым в цикле на просмотр. 
                            В противном случае возмножно наткнуться на спойлеры.</i></b><br>
                            <br>
                            {description.strip() if description else "Описание отсутствует."}
                        ''',
        author_name=account['author_name'],
        author_url=account['author_url']
    )

    return page['url']

