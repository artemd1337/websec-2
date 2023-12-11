import sqlite3

conn = sqlite3.connect('database.sqlite3')
conn.execute('CREATE TABLE groups (id INTEGER unique, name TEXT);')
conn.execute('CREATE TABLE teachers (id INTEGER unique, name TEXT);')
conn.close()