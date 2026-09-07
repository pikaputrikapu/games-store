import sys
from PyQt6.QtWidgets import QApplication
from games_widget import GamesWidget

def main():
    app = QApplication(sys.argv)
    window = GamesWidget()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()