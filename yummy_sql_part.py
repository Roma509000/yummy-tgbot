import sqlite3


def get_random(higher_rate=False):
    connection = sqlite3.connect('yummy_data.db')
    cursor = connection.cursor()

    if higher_rate:
        cursor.execute('SELECT * FROM yummy WHERE rate >= 9 ORDER BY random() LIMIT 1')
    else:
        cursor.execute('SELECT * FROM yummy ORDER BY random() LIMIT 1')

    dict_of_data = {}
    unorganised_data = cursor.fetchone()
    keys = ['name', 'rate', 'status', 'year', 'category', 'type', 'description', 'url', 'poster_url']
    for key, data in zip(keys, unorganised_data):
        dict_of_data[key] = data

    connection.close()

    return dict_of_data
