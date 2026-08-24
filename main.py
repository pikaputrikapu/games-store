import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QMessageBox, QAbstractItemView
from database import get_all_games, add_game, delete_game_by_id


class MainWindow(QWidget):
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

        self.game_table = QTableWidget()
        self.game_table.setColumnCount(4)
        self.game_table.setHorizontalHeaderLabels(["ID", "Название", "Жанр", "Цена"])
        self.game_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        layout = QVBoxLayout()
        layout.addWidget(self.lable)
        layout.addLayout(input_layout)
        layout.addWidget(self.game_table)
        self.setLayout(layout)
        self.refresh_button = QPushButton("Обновить", self)
        self.refresh_button.clicked.connect(self.refresh_games)
        layout.addWidget(self.refresh_button)
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

        add_game(title, genre, price_text)
        QMessageBox.information(self, "Успех", f"Игра {title} добавлена")
        self.title_input.clear()
        self.genre_input.clear()
        self.price_input.clear()
        self.refresh_games()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())