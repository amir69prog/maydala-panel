import sys
from pathlib import Path
from typing import List

from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout
from PyQt5.uic import loadUi

from core.models import *
from core.query import * 
from core.session import session


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / 'application'


class HomePage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/home.ui', self)
        self.setFixedSize(800,500)

        # Signals
        self.products_btn.clicked.connect(self.clicked_product_view)
        self.carts_btn.clicked.connect(self.clicked_cart_view)


    def clicked_product_view(self):
        """ Set Product View """
        stacked_layout.setCurrentIndex(1)

    def clicked_cart_view(self):
        """ Set Add Cart View """
        stacked_layout.setCurrentIndex(2)


class AddProductView(QWidget):

    def __init__(self, persons: List[Person]) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/add_product_view.ui', self)
        self.setFixedSize(800,500)


class AddCartView(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/add_cart.ui', self)
        self.setFixedSize(800,500)



############### Run

if __name__ == '__main__':
    persons = query_all_person(session)
    app = QApplication(sys.argv)

    home_page = HomePage()
    add_product_view = AddProductView()
    add_cart_view = AddCartView(persons)
    
    stacked_layout = QStackedLayout()
    stacked_layout.insertWidget(0, home_page)
    stacked_layout.insertWidget(1, add_product_view)
    stacked_layout.insertWidget(2, add_cart_view)

    app.exec()