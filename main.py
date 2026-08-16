import database

# #Get all games
# print("=== GAMES ===")
# games = database.get_all_games()
# for game in games:
#     print (f"{game['id']}, {game['title']}, {game['genre']}, {game['price']}")


# #Get all customers
# print("=== CUSTOMERS ===")
# customers = database.get_all_customers()
# for customer in customers:
#     print(f"{customer['id']}, {customer['name']}, {customer['age']}, {customer['email']}, {customer['phone']}")

# #Get game by id
# print("=== GAME BY ID ===")
# game_id = database.get_game_by_id(1)
# if game_id: print(f"{game_id['id']}, {game_id['title']}, {game_id['genre']}, {game_id['price']}")
# else: print("игра не найдена")

# #Get customer by id
# print("=== CUSTOMER BY ID ===")
# customer_id = database.get_customer_by_id(1)
# if customer_id: print(f"{customer_id['id']},{customer_id['name']},{customer_id['age']},{customer_id['email']},{customer_id['phone']}")
# else: print("Клиент не найден")

# #Get customers count
# print("=== CUSTOMERS COUNT ===")
# customers_count = database.count_customers()
# print(customers_count) 

# #Get games count
# print("=== GAMES COUNT ===")
# games_count = database.count_games()
# print(games_count)

# #Add game
# print("=== ADDED GAME ===")
# added_game = database.add_game("test_title", "test_genre", 20)
# print(added_game)

# #Add customer
# print("=== ADDED CUSTOMER ===")
# added_customer = database.add_customer("test_name", 20, "test_email", +75937247403)
# print(added_customer)

# #Delete game by id
# print("=== DELETED GAME ===")
# deleted_game = database.delete_game_by_id(1)
# if deleted_game: print(f"{deleted_game["id"]}, {deleted_game["title"]}, {deleted_game["genre"]}, {deleted_game["price"]}")

# #Delete customer by id
# print("=== DELETED CUSTOMER ===")
# deleted_customer = database.delete_customer_by_id(1)
# if deleted_customer: print(f"{deleted_customer["id"]}, {deleted_customer["name"]}, {deleted_customer["email"]}, {deleted_customer["phone"]}")
# else: print(f"Пользователь не найден")

# #Get game by title
# print("=== GAME BY TITLE ===")
# game_by_title = database.get_game_by_title("Baba Is You")
# print(f"{game_by_title['id']},{game_by_title['title']},{game_by_title['genre']},{game_by_title['price']}")

# #Get customer by name
# print("=== CUSTOMER BY NAME ===")
# customer_by_name = database.get_customer_by_name("Alex")
# print(f"{customer_by_name['id']},{customer_by_name['name']},{customer_by_name['email']},{customer_by_name['phone']}")