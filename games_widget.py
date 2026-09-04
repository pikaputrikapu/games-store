from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton,
QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QMessageBox, QAbstractItemView)
from database import get_all_games, add_game, delete_game_by_id, update_game
from edit_game_dialog import EditGameDialog


class GamesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Store")
        self.resize(800, 600)
        self.lable = QLabel("Магазин игр", self)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название игры")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр игры")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена игры")
        self.add_button = QPushButton("Добавить игру", self)
        self.add_button.clicked.connect(self.add_new_game)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.title_input)
        input_layout.addWidget(self.genre_input)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(self.add_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.search_input.textChanged.connect(self.search_games)

        self.game_table = QTableWidget()
        self.game_table.setColumnCount(4)
        self.game_table.setHorizontalHeaderLabels(["ID", "Название", "Жанр", "Цена"])
        self.game_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.game_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.game_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.delete_button = QPushButton("Удалить игру", self)
        self.delete_button.clicked.connect(self.delete_selected_game)
        self.refresh_button = QPushButton("Обновить", self)
        self.refresh_button.clicked.connect(self.refresh_games)
        self.update_button = QPushButton("Редактировать игру", self)
        self.update_button.clicked.connect(self.update_selected_game)
        
        layout = QVBoxLayout()
        layout.addWidget(self.lable)
        layout.addLayout(input_layout)
        layout.addWidget(self.search_input)
        layout.addWidget(self.game_table)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.refresh_games()
        

    def refresh_games(self):
        games = get_all_games()
        self.game_table.setRowCount(len(games))
        for row, game in enumerate(games):
            self.game_table.setItem(row, 0, QTableWidgetItem(str(game["id"])))
            self.game_table.setItem(row, 1, QTableWidgetItem(game["title"]))
            self.game_table.setItem(row, 2, QTableWidgetItem(game["genre"]))
            self.game_table.setItem(row, 3, QTableWidgetItem(str(game["price"])))
    
    def add_new_game(self):
        title = self.title_input.text().strip()
        genre = self.genre_input.text().strip()
        price_text = self.price_input.text().strip()

        if not title or not genre or not price_text:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполниет все поля")
            return
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть числом")
            return

        if price < 0:
            QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной")
            return

        add_game(title, genre, price)
        QMessageBox.information(self, "Успех", f"Игра {title} добавлена")
        self.title_input.clear()
        self.genre_input.clear()
        self.price_input.clear()
        self.refresh_games()

    def delete_selected_game(self):
        selected_row = self.game_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self,
            "Ошибка","Выберите игру для удаления.")
            return
        
        id_item = self.game_table.item(selected_row, 0)
        title_item = self.game_table.item(selected_row, 1)
        game_id = int(id_item.text())
        game_title = title_item.text()
        answer = QMessageBox.question(self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить игру '{game_title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            delete_game_by_id(game_id)
            QMessageBox.information(self, "Успех", f"Игра '{game_title}' удалена.")
            self.refresh_games()

    def update_selected_game(self):
        selected_row = self.game_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,
            "Ошибка", "Пожалуйста, выберите игру для редактирования.")
            return
        id_item = int(self.game_table.item(selected_row, 0).text())
        title_item = self.game_table.item(selected_row, 1).text()
        genre_item = self.game_table.item(selected_row, 2).text()
        price_item = self.game_table.item(selected_row, 3).text()

        dialog = EditGameDialog(id_item, title_item, genre_item, price_item, self)


        if not dialog.exec():
            return
        
        new_title, new_genre, new_price_text = dialog.get_data()

        if not new_title:
            new_title = title_item
        if not new_genre:
            new_genre = genre_item
        if not new_price_text:
            new_price = float(price_item)
        else:
            try:
                new_price = float(new_price_text)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Цена должна быть числом")
                return
            if new_price < 0:
                QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной")
                return
            update_game(id_item, new_title, new_genre, new_price)
            QMessageBox.information(self, "Успех", f"Данные игры {new_title} обновлены")
            self.refresh_games()

    def search_games(self):
        search_text = self.search_input.text().strip().lower()
        for row in range(self.game_table.rowCount()):
            title_item = self.game_table.item(row, 1)
            game_title = title_item.text().lower()

            if search_text in game_title:
                self.game_table.setRowHidden(row, False)
            else:
                self.game_table.setRowHidden(row, True)