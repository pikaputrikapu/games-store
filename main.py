import sys
from PyQt6.QtWidgets import QApplication
from games_widget import GamesWidget

app = QApplication(sys.argv)

window = GamesWidget()
window.show()

sys.exit(app.exec())