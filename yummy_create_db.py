import sqlite3

# creating data base
connection = sqlite3.connect('yummy_database.db')

cursor = connection.cursor()

cursor.execute("CREATE TABLE yummybot (name TEXT, rate TEXT, status TEXT, year TEXT, categories TEXT, type TEXT, description TEXT, url TEXT, poster_url TEXT, desc_page TEXT)")

connection.close()




