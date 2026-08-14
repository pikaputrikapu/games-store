import database

# print("=== ИГРЫ ===")
# games = database.get_all_games()
# for game in games:
#     print (f"{game['id']}, {game['title']}, {game['genre']}, {game['price']}")

#Выводит все игры
# #Выводит всех клиентов
# print("=== КЛИЕНТЫ ===")
# customers = database.get_all_customers()
# for customer in customers:
#     print(f"{customer['id']}, {customer['name']}, {customer['age']}, {customer['email']}, {customer['phone']}")

# #Выводит игру по id
# print("=== ИГРА ===")
# game_id = database.get_game_by_id(1)
# if game_id: print(f"{game_id['id']}, {game_id['title']}, {game_id['genre']}, {game_id['price']}")
# else: print("игра не найдена")

# #Выводит клиента по id
# print("=== КЛИЕНТ ===")
# customer_id = database.get_customer_by_id(1)
# if customer_id: print(f"{customer_id['id']},{customer_id['name']},{customer_id['age']},{customer_id['email']},{customer_id['phone']}")
# else: print("Клиент не найден")

# print("=== КОЛИЧЕСТВО КЛИЕНТОВ ===")
# customers_count = database.count_customers()
# print(customers_count) 

# #Выводит количесвто игр
# print("=== КОЛИЧЕСТВО ИГР ===")
# games_count = database.count_games()
# print(games_count)

#Добавляет игру
# print("=== ДОБАВЛЕНА ИГРА ===")
# added_game = database.add_game("test_title", "test_genre", 20)
# print(added_game)

# #Добавляет клиента
# print("=== ДОБАВЛЕН КЛИЕНТ ===")
# added_customer = database.add_customer("test_name", 20, "test_email", +75937247403)
# print(added_customer)