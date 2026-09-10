from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton,
QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QMessageBox, QAbstractItemView)
from database import get_all_games, add_game, delete_game_by_id, update_game
from edit_game_dialog import EditGameDialog


class GamesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Store")
        self.resize(800, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.dark_theme_active = False

        self.create_widgets()
        self.setup_layout()
        self.connect_signals()
        self.setup_style()

        self.refresh_games()

    def create_widgets(self):
        self.lable = QLabel("Магазин игр", self)
        self.lable.setObjectName("titleLabel")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название игры")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр игры")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена игры")

        self.add_button = QPushButton("Добавить игру", self)
        self.add_button.setObjectName("addButton")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")

        self.game_table = QTableWidget()
        self.game_table.setColumnCount(4)
        self.game_table.setHorizontalHeaderLabels(["ID", "Название", "Жанр", "Цена"])
        self.game_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.game_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.game_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.delete_button = QPushButton("Удалить игру", self)
        self.delete_button.setObjectName("deleteButton")

        self.refresh_button = QPushButton("Обновить", self)
        self.refresh_button.setObjectName("refreshButton")

        self.update_button = QPushButton("Редактировать игру", self)
        self.update_button.setObjectName("updateButton")

        self.theme_button = QPushButton("Тёмная тема", self)
        self.theme_button.setObjectName("themeToggleButton")

    def setup_layout(self):
        add_panel_layout = QHBoxLayout()
        add_panel_layout.addWidget(self.title_input)
        add_panel_layout.addWidget(self.genre_input)
        add_panel_layout.addWidget(self.price_input)
        add_panel_layout.addWidget(self.add_button)

        actions_layout = QHBoxLayout()
        actions_layout.addWidget(self.update_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addWidget(self.refresh_button)
        actions_layout.addWidget(self.theme_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(self.lable)
        layout.addLayout(add_panel_layout)
        layout.addWidget(self.search_input)
        layout.addWidget(self.game_table)
        layout.addLayout(actions_layout)

        self.setLayout(layout)

    def connect_signals(self):
        self.update_button.clicked.connect(self.update_selected_game)
        self.refresh_button.clicked.connect(self.refresh_games)
        self.delete_button.clicked.connect(self.delete_selected_game)
        self.add_button.clicked.connect(self.add_new_game)
        self.search_input.textChanged.connect(self.search_games)
        self.theme_button.clicked.connect(self.toggle_theme)

    LIGHT_ROW_COLOR = QColor("#F2F9FE")  # светло-светло-голубой
    DARK_ROW_COLOR = QColor("#232B33")   # тёмно-синий (для тёмной темы)

    @property
    def row_color(self):
        return self.DARK_ROW_COLOR if self.dark_theme_active else self.LIGHT_ROW_COLOR

    def refresh_games(self):
        games = get_all_games()
        self.game_table.setRowCount(len(games))
        for row, game in enumerate(games):
            id_item = QTableWidgetItem(str(game["id"]))
            title_item = QTableWidgetItem(game["title"])
            genre_item = QTableWidgetItem(game["genre"])
            price_item = QTableWidgetItem(str(game["price"]))
            for item in (id_item, title_item, genre_item, price_item):
                item.setBackground(self.row_color)
            self.game_table.setItem(row, 0, id_item)
            self.game_table.setItem(row, 1, title_item)
            self.game_table.setItem(row, 2, genre_item)
            self.game_table.setItem(row, 3, price_item)
        self.search_games()
    
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

    def setup_style(self):
        self._apply_theme()

    def _apply_theme(self):
        filename = "stylesDark.qss" if self.dark_theme_active else "stylesLight.qss"
        styles_path = Path(__file__).parent / filename
        styles = styles_path.read_text(encoding="utf-8")
        self.setStyleSheet(styles)

    def toggle_theme(self):
        self.dark_theme_active = not self.dark_theme_active
        self.theme_button.setText("☀ Светлая тема" if self.dark_theme_active else "🌙 Тёмная тема")
        self._apply_theme()
        self.refresh_games()