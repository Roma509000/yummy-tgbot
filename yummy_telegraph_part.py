from telegraph.aio import Telegraph


async def create_page(name, description):
    telegraph = Telegraph(access_token='556e3c7105b489aa646515a5b8d6eabd32641a2447b933e36d7a9f0198ac')
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

    print(page['url'])
    return page['url']

