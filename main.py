import sys
from pathlib import Path
from typing import List

from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from core.models import *
from core import query 
from core import utils
from core.session import session


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / 'application'


### Functions ###

def back_to_pervious_page(pervious_page_index: int):
    """ Back to previous page """
    stacked_layout.setCurrentIndex(pervious_page_index)

def go_to_home_page():
    """ Go to Home Page """
    stacked_layout.setCurrentWidget(home_page)

def go_to_settings_page():
    """ Go to Settings Page """
    stacked_layout.setCurrentWidget(settings_page)

def close_app():
    """ Close App """
    sys.exit(app.exec_())

def go_to_person_page():
    """ Go to Person Page """
    stacked_layout.setCurrentWidget(person_page)

def go_to_order_page():
    """ Go to Order Page """
    # stacked_layout.setCurrentIndex(2)

def go_to_product_page():
    """ Go to Prodcut Page """
    # stacked_layout.setCurrentIndex(3)

def validete_form(form_data):
    """ Validate Form """
    for key, value in form_data.items():
        if len(str(value)) < 3:
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
        self.settings_btn.clicked.connect(go_to_settings_page)
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
            person_page.update_person_table()


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
        person_id = self.person_table.item(item.row(), 0).text()
        person = query.query_person_by_id(session, person_id)
        person_widget = PersonWidget(person)
        stacked_layout.addWidget(person_widget)
        stacked_layout.setCurrentWidget(person_widget)


class FormWidget(QWidget):

    def __init__(self, form: Form) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/form_widget.ui', self)
        self.form = form
        self.settings()
        self.init_ui()

        # Signals
        self.edit_btn.clicked.connect(self.edit_form)
        self.cancel_edit_btn.clicked.connect(self.cancel_edit)

    def settings(self):
        """ Settings """
        self.setFixedSize(332,145)
        self.setWindowTitle(f'Form: {self.form.title}')
    
    def init_ui(self):
        """ Initialize UI """
        self.title_input.setText(self.form.title)
        self.base_price_input.setValue(int(self.form.base_price))
    
    def edit_form(self):
        """ Edit form """
        self.form.title = self.title_input.text()
        self.form.base_price = self.base_price_input.value()
        data = {
            'title': self.form.title,
            'base_price': self.form.base_price
        }
        is_valid = validete_form(data)
        if is_valid:
            utils.edit_form(session, self.form.id, **data)
            settings_page.update_form_table()
            go_to_settings_page()
    
    def cancel_edit(self):
        """ Cancel edit """
        go_to_settings_page()


class ColorWidget(QWidget):
    
    def __init__(self, color: Color) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/color_widget.ui', self)
        self.color = color
        self.settings()
        self.init_ui()

        # Signals
        self.edit_btn.clicked.connect(self.edit_color)
        self.cancel_edit_btn.clicked.connect(self.cancel_edit)
    
    def settings(self):
        """ Settings """
        self.setFixedSize(332,145)
        self.setWindowTitle(f'Color: {self.color.color}')
    
    def init_ui(self):
        """ Initialize UI """
        self.color_input.setText(self.color.color)
    
    def edit_color(self):
        """ Edit color """
        self.color.color = self.color_input.text()
        data = {
            'color': self.color.color
        }
        is_valid = validete_form(data)
        if is_valid:
            utils.edit_color(session, self.color.id, **data)
            settings_page.update_color_table()
            go_to_settings_page()
        
    def cancel_edit(self):
        """ Cancel edit """
        go_to_settings_page()


class SettingsPage(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/settings.ui', self)
        self.init_form_ui()
        self.init_color_ui()
        self.settings()

        # Signals
        self.add_form_btn.clicked.connect(self.add_form)
        self.add_color_btn.clicked.connect(self.add_color)
        self.form_table.itemClicked.connect(self.going_to_delete_or_edit_form)
        self.delete_form_btn.clicked.connect(self.delete_form)
        self.cancel_form_btn.clicked.connect(self.init_form_ui)
        self.edit_form_btn.clicked.connect(self.edit_form_widget)
        self.color_table.itemClicked.connect(self.going_to_delete_or_edit_color)
        self.delete_color_btn.clicked.connect(self.delete_color)
        self.cancel_color_btn.clicked.connect(self.init_color_ui)
        self.edit_color_btn.clicked.connect(self.edit_color_widget)
                
    def init_form_ui(self):
        """ Initialize Form UI """
        self.update_form_table()
        self.cancel_form_btn.setEnabled(False)
        self.delete_form_btn.setEnabled(False)
        self.edit_form_btn.setEnabled(False)

    def init_color_ui(self):
        """ Initialize Color UI """
        self.update_color_table()
        self.cancel_color_btn.setEnabled(False)
        self.delete_color_btn.setEnabled(False)
        self.edit_color_btn.setEnabled(False)

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle('Settings')
    
    def update_form_table(self):
        """ Update form table """
        self.form_table.setRowCount(0)
        forms = query.query_all_form(session)
        row_count = self.form_table.rowCount()
        for form in forms:
            self.form_table.insertRow(row_count)
            item_id = QTableWidgetItem(str(form.id))
            self.form_table.setItem(row_count, 0, item_id)
            item_id.setFlags(Qt.ItemIsEnabled)
            self.form_table.setItem(row_count, 1, QTableWidgetItem(form.title))
            self.form_table.setItem(row_count, 2, QTableWidgetItem(str(form.base_price)))
            row_count += 1
    
    def add_form(self):
        """ Add a new form """
        title = self.title_input.text()
        base_price = self.base_price_input.text()
        data = {
            'title': title,
            'base_price': base_price
        }
        is_valid = validete_form(data)
        if is_valid:
            utils.add_form(session, **data)
            self.title_input.clear()
            self.base_price_input.clear()
            self.update_form_table()

    def going_to_delete_or_edit_form(self):
        """ Going to Delete a form """
        self.delete_form_btn.setEnabled(True)
        self.cancel_form_btn.setEnabled(True)
        self.edit_form_btn.setEnabled(True)
    
    def delete_form(self):
        """ Delete a form """
        form_id = self.form_table.item(self.form_table.currentRow(), 0).text()
        utils.delete_form(session, form_id)
        self.init_form_ui()
    
    def edit_form_widget(self):
        """ Edit form widget """
        form_id = self.form_table.item(self.form_table.currentRow(), 0).text()
        form = query.query_form_by_id(session, form_id)
        form_widget = FormWidget(form)
        stacked_layout.addWidget(form_widget)
        stacked_layout.setCurrentWidget(form_widget)
    
    def update_color_table(self):
        """ Update color table """
        self.color_table.setRowCount(0)
        colors = query.query_all_color(session)
        row_count = self.color_table.rowCount()
        for color in colors:
            self.color_table.insertRow(row_count)
            item_id = QTableWidgetItem(str(color.id))
            self.color_table.setItem(row_count, 0, item_id)
            item_id.setFlags(Qt.ItemIsEnabled)
            self.color_table.setItem(row_count, 1, QTableWidgetItem(color.color))
            row_count += 1

    def add_color(self):
        """ Add a new color """
        color = self.color_input.text()
        data = {
            'color': color
        }
        is_valid = validete_form(data)
        if is_valid:
            utils.add_color(session, **data)
            self.color_input.clear()
            self.update_color_table() 
    
    def going_to_delete_or_edit_color(self):
        """ Going to Delete a color """
        self.delete_color_btn.setEnabled(True)
        self.cancel_color_btn.setEnabled(True)
        self.edit_color_btn.setEnabled(True)
    
    def delete_color(self):
        """ Delete a color """
        color_id = self.color_table.item(self.color_table.currentRow(), 0).text()
        utils.delete_color(session, color_id)
        self.init_color_ui()
    
    def edit_color_widget(self):
        """ Edit color widget """
        color_id = self.color_table.item(self.color_table.currentRow(), 0).text()
        color = query.query_color_by_id(session, color_id)
        color_widget = ColorWidget(color)
        stacked_layout.addWidget(color_widget)
        stacked_layout.setCurrentWidget(color_widget)


### End Pages ###


### Run ###

if __name__ == '__main__':
    app = QApplication(sys.argv)

    home_page = HomePage()
    person_page = PersonPage()
    settings_page = SettingsPage()
    
    stacked_layout = QStackedLayout()
    stacked_layout.addWidget(home_page)
    stacked_layout.addWidget(person_page)
    stacked_layout.addWidget(settings_page)

    app.exec()

### End Run ###