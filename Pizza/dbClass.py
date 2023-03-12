import sqlite3 as sql

db = sql.connect('pizza.db')
im = db.cursor()