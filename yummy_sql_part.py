import sqlite3


def get_random():
    connection = sqlite3.connect('yummy_data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM yummy ORDER BY random() LIMIT 1')

    dict_of_data = {}
    unorganised_data = cursor.fetchone()
    keys = ['name', 'rate', 'status', 'year', 'category', 'type', 'description', 'url', 'poster_url']
    for key, data in zip(keys, unorganised_data):
        dict_of_data[key] = data

    connection.close()

    return dict_of_data
