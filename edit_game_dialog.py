from PyQt6.QtWidgets import (QLineEdit,
QDialog, QFormLayout, QDialogButtonBox)


class EditGameDialog(QDialog):
    def __init__(self, game_id, title, genre, price, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Редактировать игру")

        self.game_id = game_id

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText(f"Сейчас: {title}")

        self.genre_edit = QLineEdit()
        self.genre_edit.setPlaceholderText(f"Сейчас: {genre}")

        self.price_edit = QLineEdit()
        self.price_edit.setPlaceholderText(f"Сейчас: {price}")

        form_layout = QFormLayout()
        form_layout.addRow("Название:", self.title_edit)
        form_layout.addRow("Жанр:", self.genre_edit)
        form_layout.addRow("Цена:", self.price_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )        
        
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        form_layout.addWidget(buttons)
        self.setLayout(form_layout)


    def get_data(self):
        return (
            self.title_edit.text().strip(),
            self.genre_edit.text().strip(),
            self.price_edit.text().strip()
        )