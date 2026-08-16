import sqlite3


DB_NAME = 'game_store.db'

def get_connection() -> sqlite3.Connection:
    """Подключение к базе данных с нужными настройками"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def get_all_games():
    """Получение всех игр"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games;")
    games = cursor.fetchall()
    conn.close()
    return games

def get_all_customers():
    """Получение всех пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers;")
    customers = cursor.fetchall()
    conn.close
    return customers

def get_game_by_id(game_id):
    """Получение игры по id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE id = ?;", (game_id,))
    game_by_id = cursor.fetchone()
    conn.close()
    return game

def get_game_by_title(game_title):
    """Получение игры по title"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE title = ?;", (game_title,))
    game_by_title = cursor.fetchone()
    conn.close()
    return game_by_title

def get_customer_by_name(customer_name):
    """Получение пользователя по name"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE name = ?;", (customer_name,))
    customer_by_name = cursor.fetchone()
    cursor.close()
    return customer_by_name

def get_customer_by_id(customer_id):
    """Получение пользователя по id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?;", (customer_id,))
    customer_by_id = cursor.fetchone()
    conn.close()
    return customer

def count_customers():
    """Получение количества пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]
    conn.close()
    return customers

def count_games():
    """Получение количества игр"""
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
    """Добавляет пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", (name, age, email, phone))
    conn.commit()
    conn.close()
    return f"{name} {age} {email} {phone}"

def delete_game_by_id(game_id):
    """Удаляет игру по id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games WHERE id = ?;",(game_id,))
    deleted_game = cursor.fetchone()
    cursor.execute("DELETE FROM games WHERE id = ?;",(game_id,))
    conn.commit()
    conn.close()
    return deleted_game

def delete_customer_by_id(customer_id):
    """Удаляет пользователя по id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?;",(customer_id,))
    deleted_customer = cursor.fetchone()
    cursor.execute("DELETE FROM customers WHERE id = ?;",(customer_id,))
    conn.commit()
    conn.close()
    return deleted_customer

