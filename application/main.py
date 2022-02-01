import sys
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget
from PyQt5.uic import loadUi


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / 'application'


class HomePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/home.ui',self)
        self.setFixedSize(800,500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.show()
    app.exec()