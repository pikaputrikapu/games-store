import sqlite3
import random


DB_NAME = 'game_store.db'

def get_connection() -> sqlite3.Connection:
    """Подключение к базе данных с нужными настройками"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=(), fetch=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = None
    if fetch == 'one':
        result = cursor.fetchone()
    elif fetch == 'all':
        result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def get_all_games():
    """Получение всех игр"""
    return execute_query("SELECT * FROM games;", fetch='all')

def get_all_customers():
    """Получение всех пользователей"""
    return execute_query("SELECT * FROM customers;", fetch='all')

def get_game_by_id(game_id):
    """Получение игры по id"""
    return execute_query("SELECT * FROM games WHERE id = ?;", (game_id,), fetch='one')

def get_game_by_title(game_title):
    """Получение игры по title"""
    return execute_query("SELECT * FROM games WHERE title = ?;", (game_title,), fetch='one')

def get_customer_by_name(customer_name):
    """Получение пользователя по name"""
    return execute_query("SELECT * FROM customers WHERE name = ?;", (customer_name,), fetch='one')

def get_customer_by_id(customer_id):
    """Получение пользователя по id"""
    return execute_query("SELECT * FROM customers WHERE id = ?;", (customer_id,), fetch='one')

def count_customers():
    """Получение количества пользователей"""
    return execute_query("SELECT COUNT(*) FROM customers", fetch='one')[0]

def count_games():
    """Получение количества игр"""
    return execute_query("SELECT COUNT(*) FROM games", fetch='one')[0]

def add_game(title, genre, price):
    """Добавляет игру"""
    execute_query("INSERT INTO games (title, genre, price) VALUES (?, ?, ?)", (title, genre, price), fetch='one')
    added_game = f"{title}, {genre}, {price}"
    return added_game

def add_customer(name, age, email, phone, coins):
    """Добавляет пользователя"""
    execute_query("INSERT INTO customers (name, age, email, phone, coins) VALUES (?, ?, ?, ?, ?)", (name, age, email, phone, coins), fetch='one')
    added_customer = f"{name}, {age}, {email}, {phone}, {coins}"
    return added_customer

def delete_game_by_id(game_id):
    """Удаляет игру по id"""
    deleted_game = execute_query("SELECT * FROM games WHERE id = ?;", (game_id,), fetch='one')
    execute_query("DELETE FROM games WHERE id = ?;", (game_id,), fetch='one')
    return deleted_game

def delete_customer_by_id(customer_id):
    """Удаляет пользователя по id"""
    deleted_customer = execute_query("SELECT * FROM customers WHERE id = ?;", (customer_id,), fetch='one')
    execute_query("DELETE FROM customers WHERE id = ?;", (customer_id,))
    return deleted_customer

def get_customer_purchases(customer_id):
    """Получение покупок пользователя"""
    return execute_query("""
        SELECT purchases.id, games.title, purchases.purchase_date, purchases.price
        FROM purchases
        JOIN games ON purchases.game_id = games.id
        WHERE purchases.customer_id = ?
        ORDER BY purchases.purchase_date DESC;""",
        (customer_id,), fetch='all')

def get_game_buyers(game_id):
    """Получение покупателей игры"""
    return execute_query("""
        SELECT customers.id, customers.name, customers.age, customers.email, customers.phone
        FROM purchases
        JOIN customers ON purchases.customer_id = customers.id
        WHERE purchases.game_id = ?
        ORDER BY purchases.purchase_date DESC""",
        (game_id,), fetch='all')


def get_all_genres():
    return execute_query("""
    SELECT DISTINCT genre
    FROM games
    ORDER BY genre;""",
    fetch='all')

def get_filtered_games(title='',genre="Все жанры"):
    query = "SELECT * FROM games WHERE title LIKE ?"
    params = [f"%{title}%"]
    if genre != "Все жанры":
        query += " AND genre = ?"
        params.append(genre)
    query += " ORDER BY title;"
    return execute_query(query, params, fetch="all")

def add_purches(game_id, customer_id):
    price = int(execute_query("SELECT price FROM games WHERE id = ?;",(game_id,), fetch='one')['price'])
    customer = execute_query("SELECT coins FROM customers WHERE id = ?;", (customer_id,), fetch='one')
    if customer is None or customer['coins'] < price:
        return "на аккаунте не достачно монет"
    existing = execute_query(
        "SELECT id FROM purchases WHERE customer_id = ? AND game_id = ?;",
        (customer_id, game_id), fetch='one')
    if existing:
        return "игра уже куплена"
    date = f"2026-{random.randint(1, 12):02}-{random.randint(1, 28):02d}"
    execute_query(
        "INSERT INTO purchases (customer_id, game_id, purchase_date, price) VALUES (?, ?, ?, ?);",
        (customer_id, game_id, date, price))
    execute_query(
        "UPDATE customers SET coins = coins - ? WHERE id = ?;",
        (price, customer_id))
    return "покупка прошла успешно"

def delete_purchase(purchase_id):
    """Удаляет покупку по id"""
    deleted_purchase = execute_query("SELECT * FROM purchases WHERE id = ?;", (purchase_id,), fetch='one')
    execute_query("DELETE FROM purchases WHERE id = ?;", (purchase_id,))
    return deleted_purchase