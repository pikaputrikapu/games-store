import sqlite3 
import random

DB_NAME = "game_store.db"

random.seed(42)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.executescript("""
    DROP TABLE IF EXISTS purchases;
    DROP TABLE IF EXISTS games;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT
        );

    CREATE TABLE games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        price TEXT NOT NULL
        );

    CREATE TABLE purchases (
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        purchase_date TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
        );        
    """)

    names = [
        "Anna", "Boris", "Max", "Alex", "Kate", "Ivan", "Dmitry", "Olga",
        "Pavel", "Nina", "Sergey", "Lena", "Vlad", "Sonia", "Roman", "Tanya",
        "Igor", "Vera", "Denis", "Masha", "Artem", "Yulia", "Kirill", "Dasha",
        "Anton", "Galina", "Leon", "Polina", "Gleb", "Rita",
    ]
    games = [
        ("Stardew Valley", "Simulation", 14),
        ("Hollow Knight", "Platformer", 15),
        ("Celeste", "Platformer", 20),
        ("Hades", "Roguelike", 25),
        ("The Witcher 3", "RPG", 40),
        ("Skyrim", "RPG", 30),
        ("Doom Eternal", "Shooter", 60),
        ("Cuphead", "Platformer", 20),
        ("Dead Cells", "Roguelike", 25),
        ("Rimworld", "Simulation", 35),
        ("Civilization VI", "Strategy", 60),
        ("Among Us", "Party", 5),
        ("Fall Guys", "Party", 19),
        ("Rocket League", "Sports", 10),
        ("Valheim", "Survival", 20),
        ("Subnautica", "Adventure", 30),
        ("Outer Wilds", "Adventure", 25),
        ("Disco Elysium", "RPG", 40),
        ("Slay the Spire", "Roguelike", 25),
        ("Baba Is You", "Puzzle", 15),
        ("The Binding of Isaac", "Roguelike", 15),
        ("Ori and the Blind Forest", "Platformer", 20),
        ("Undertale", "RPG", 10),
        ("Katana Zero", "Action", 15),
        ("Vampire Survivors", "Roguelike", 5),
        ("Elden Ring", "RPG", 60),
        ("Cyberpunk 2077", "RPG", 50),
        ("Sekiro", "Action", 60),
        ("Frostpunk", "Strategy", 30),
        ("Papers Please", "Simulation", 10),
    ]
    customers = []
    for name in names:
        age = random.randint(12, 80)
        email = f"{name.lower()}@yandex.ru"
        phone = f"+7{random.randint(1000000000, 9999999999)}"
        customers.append((name, age, email, phone))

    

    cursor.executemany("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?);", customers)
    cursor.executemany("INSERT INTO games (title, genre, price) VALUES (?, ?, ?);", games)

    for _ in range(30):
        customers_id = random.randint(1, len(games))
        date = f"2026-{random.randint(1, 12):02}-{random.randint(1, 28):02d}"
        game_id = random.sample(range(1, len(games) + 1), 1)[0]
        price = games[game_id - 1][2]
        cursor.execute(
            "INSERT INTO purchases (customer_id, game_id, purchase_date, price) VALUES (?, ?, ?, ?);",
            (customers_id, game_id, date, price)
        )
    conn.commit()
    conn.close()

    print("Таблички были сброшенны")

init_db()