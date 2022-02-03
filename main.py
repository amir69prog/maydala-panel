import sys
from pathlib import Path
from typing import List

from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout, QTableWidgetItem
from PyQt5.uic import loadUi

from core.models import *
from core import query 
from core import utils
from core.session import session


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / 'application'


### Functions ###

def go_to_home_page():
    """ Go to Home Page """
    stacked_layout.setCurrentIndex(0)

def close_app():
    """ Close App """
    sys.exit(app.exec_())

def go_to_person_page():
    """ Go to Person Page """
    stacked_layout.setCurrentIndex(1)

def go_to_order_page():
    """ Go to Order Page """
    stacked_layout.setCurrentIndex(2)

def go_to_product_page():
    """ Go to Prodcut Page """
    stacked_layout.setCurrentIndex(3)

def validete_form(form_data):
    """ Validate Form """
    if len(form_data['first_name']) < 3:
        return False
    if len(form_data['last_name']) < 3:
        return False
    if len(form_data['phone_number']) < 3:
        return False
    return True

### End Functions ###


### Pages ###

class HomePage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/home.ui', self)
        self.settings()
        
        # Signals
        self.person_btn.clicked.connect(go_to_person_page)
        self.orders_btn.clicked.connect(go_to_order_page)
        self.products_btn.clicked.connect(go_to_product_page)

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle(f'Home Page')



class PersonWidget(QWidget):
    
    def __init__(self, person: Person) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/person_widget.ui', self)
        self.person = person
        self.init_ui()
        self.settings()

        # Signals
        self.home_btn.clicked.connect(go_to_home_page)
        self.close_btn.clicked.connect(close_app)
        self.save_person_btn.clicked.connect(self.edit_person)
        self.edit_person_btn.clicked.connect(self.goin_to_edit_person)
        self.delete_person_btn.clicked.connect(self.delete_person)
        self.cancel_save_btn.clicked.connect(self.init_ui)

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle(f'Person: {self.person.first_name} {self.person.last_name}')

    def init_ui(self):
        """ Initialize UI """
        self.edit_person_btn.setEnabled(True)
        self.first_name_input.setText(self.person.first_name)
        self.last_name_input.setText(self.person.last_name)
        self.phone_number_input.setText(self.person.phone_number)
        self.first_name_input.setEnabled(False)
        self.last_name_input.setEnabled(False)
        self.phone_number_input.setEnabled(False)
        self.save_person_btn.setEnabled(False)
        self.cancel_save_btn.setEnabled(False)


    def goin_to_edit_person(self):
        """ Go to Edit Person Page """
        self.edit_person_btn.setEnabled(False)
        self.save_person_btn.setEnabled(True)
        self.cancel_save_btn.setEnabled(True)
        self.first_name_input.setEnabled(True)
        self.last_name_input.setEnabled(True)
        self.phone_number_input.setEnabled(True)

    def edit_person(self):
        """ Edit Person """
        self.person.first_name = self.first_name_input.text()
        self.person.last_name = self.last_name_input.text()
        self.person.phone_number = self.phone_number_input.text()
        data = {
            'first_name': self.person.first_name,
            'last_name': self.person.last_name,
            'phone_number': self.person.phone_number
        }
        is_valid = validete_form(data)
        if is_valid:
            utils.edit_person(session, self.person.person_id, **data)
            self.edit_person_btn.setEnabled(True)
            self.save_person_btn.setEnabled(False)
            self.cancel_save_btn.setEnabled(False)

        
    def delete_person(self):
        """ Delete Person """
        utils.delete_person(session, self.person.person_id)
        person_page.update_person_table()
        go_to_person_page()


class PersonPage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/person.ui', self)
        self.init_ui()
        self.settings()

        # Signals
        self.home_btn.clicked.connect(go_to_home_page)
        self.close_btn.clicked.connect(close_app)
        self.add_person_btn.clicked.connect(self.add_person)
        self.person_table.itemDoubleClicked.connect(self.detail_person_page)

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle('Person')

    def init_ui(self):
        """ Initialize UI """
        self.update_person_table() 
    
    def update_person_table(self):
        """ Update person table """
        self.person_table.setRowCount(0)
        persons = query.query_all_person(session)
        row_count = self.person_table.rowCount()
        for person in persons:
            self.person_table.insertRow(row_count)
            self.person_table.setItem(row_count, 0, QTableWidgetItem(str(person.person_id)))
            self.person_table.setItem(row_count, 1, QTableWidgetItem(person.first_name))
            self.person_table.setItem(row_count, 2, QTableWidgetItem(person.last_name))
            self.person_table.setItem(row_count, 3, QTableWidgetItem(person.phone_number))
            row_count += 1

    def add_person(self):
        """ Add a new person """
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone_number = self.phone_number_input.text()
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number
        }
        is_valid = validete_form(data)
        if is_valid:
            utils.add_person(session, **data)
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.phone_number_input.clear()
            self.update_person_table()
    
    def detail_person_page(self, item):
        """ Go to detail person page """
        person_id = self.person_table.itemAt(item.row(), 0).text()
        person = query.query_person_by_id(session, person_id)
        person_widget = PersonWidget(person)
        stacked_layout.addWidget(person_widget)
        stacked_layout.setCurrentIndex(2)

### End Pages ###


### Run ###

if __name__ == '__main__':
    app = QApplication(sys.argv)

    home_page = HomePage()
    person_page = PersonPage()
    
    stacked_layout = QStackedLayout()
    stacked_layout.insertWidget(0, home_page)
    stacked_layout.insertWidget(1, person_page)

    app.exec()

### End Run ###