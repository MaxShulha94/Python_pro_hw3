import sqlite3
import random
from faker import Faker
from flask import Flask

app = Flask(__name__)
fake = Faker()


def create_customers():
    with sqlite3.connect('customers.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS customers (
            name TEXT,
            city TEXT
        )''')
        for i in range(1, 15):
            customer_info = (fake.name(), fake.city())
            cur.execute("INSERT INTO customers (name, city) VALUES (?, ?)", customer_info)
        con.commit()


def create_tracks():
    with sqlite3.connect('tracks.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT,
            singer TEXT,
            duration TEXT,
            date TEXT
        )''')
        for i in range(0, 100):
            track_id = random.randint(1, 10000)
            singer = fake.name()
            minutes_in_sec = random.randint(1, 10) * 60
            seconds = random.randint(0, 59)
            duration = int(minutes_in_sec) + int(seconds)
            date = fake.date()
            tracks_info = (track_id, singer, duration, date)
            cur.execute("INSERT INTO tracks (track_id, singer, duration, date) VALUES (?, ?, ?, ?)", tracks_info)
        con.commit()


@app.route('/names/')
def count_unique_names():
    con = sqlite3.connect('customers.db')
    cur = con.cursor()
    unique_names = set()
    all_names = []

    for name in cur.execute('SELECT name FROM customers'):
        name = ''.join(name[0]).split(' ')
        if len(name) == 2:
            name = name[0]
        else:
            name = name[1]
        unique_names.add(name)
        all_names.append(name)
    return f'There are {len(unique_names)} unique customer`s names from {len(all_names)} names'


@app.route('/tracks/')
def count_tracks():
    con = sqlite3.connect('tracks.db')
    cur = con.cursor()
    tracks_list = []
    for i in cur.execute('SELECT singer FROM tracks'):
        tracks_list.append(i)
    return f'There are {len(tracks_list)} tracks'


@app.route('/tracks-sec/')
def get_track_info():
    con = sqlite3.connect('tracks.db')
    cur = con.cursor()
    tracks_list = []
    for i in cur.execute('SELECT track_id, singer, duration, date FROM tracks'):
        tracks_list.append(f'ID: {i[0]}; Singer`s name: {i[1]}; Duration: {i[2]} sec; Release date: {i[3]}')
    return tracks_list


if __name__ == '__main__':
    app.run()
