import sqlite3


DB_NAME = 'game_store.db'

def get_connection() -> sqlite3.Connection:
    """подключение к базе данных с нужными настройками"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def get_all_games():
    """получение всех игр из базы данных"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games;")
    games = cursor.fetchall()
    conn.close()
    return games

def get_all_customers():
    """получение всех клиентов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers;")
    customers = cursor.fetchall()
    conn.close
    return customers

def get_game_by_id(game_id):
    """получение игры по id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE id = ?;", (game_id,))
    game = cursor.fetchone()
    conn.close()
    return game

def get_customer_by_id(customer_id):
    """Получение клиента по id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?;", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def count_customers():
    """получение количества клиентов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]
    conn.close()
    return customers

def count_games():
    """получение количества игр"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM games")
    games = cursor.fetchone()[0]
    conn.close()
    return games

def add_game(title, genre, price):
    """Добавляет игру"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (title, genre, price) VALUES (?, ?, ?)",(title, genre, price))
    conn.commit()
    conn.close()
    return f"{title} {genre} {price}"

def add_customer(name, age, email, phone):
    """Добавляет клиента"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", (name, age, email, phone))
    conn.commit()
    conn.close()
    return f"{name} {age} {email} {phone}"