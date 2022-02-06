from datetime import datetime
import sys
from pathlib import Path
from typing import Dict, List

from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout, QTableWidgetItem, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QDate, QTime

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

def close_app():
    """ Close App """
    sys.exit(app.exec_())

def go_to_page(page: QWidget):
    """ Go to specefic page """
    stacked_layout.setCurrentWidget(page)

def validete_form(form_data, non_required: List = None):
    """ Validate Form """
    for key, value in form_data.items():
        if non_required:
            if (not value or value == '') and key in non_required:
                continue
        if not value:
            print(f'{key, value} is empty')
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
        self.person_btn.clicked.connect(lambda :go_to_page(person_page))
        self.orders_btn.clicked.connect(lambda :go_to_page(order_page))
        self.settings_btn.clicked.connect(lambda :go_to_page(settings_page))

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle(f'صفحه اصلی')



class PersonWidget(QWidget):
    
    def __init__(self, person: Person) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/person_widget.ui', self)
        self.person = person
        self.init_ui()
        self.settings()

        # Signals
        self.home_btn.clicked.connect(lambda :go_to_page(home_page))
        self.close_btn.clicked.connect(close_app)
        self.save_person_btn.clicked.connect(self.edit_person)
        self.edit_person_btn.clicked.connect(self.goin_to_edit_person)
        self.delete_person_btn.clicked.connect(self.delete_person)
        self.cancel_save_btn.clicked.connect(self.init_ui)

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle(f'مشتری: {self.person.first_name} {self.person.last_name}')

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
            add_bookmark_page.update_person_combo()
            add_board_page.update_person_combo()

    def delete_person(self):
        """ Delete Person """
        utils.delete_person(session, self.person.person_id)
        person_page.update_person_table()
        add_bookmark_page.update_person_combo()
        add_board_page.update_person_combo()
        go_to_page(person_page)


class PersonPage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/person.ui', self)
        self.init_ui()
        self.settings()

        # Signals
        self.home_btn.clicked.connect(lambda :go_to_page(home_page))
        self.close_btn.clicked.connect(close_app)
        self.add_person_btn.clicked.connect(self.add_person)
        self.person_table.itemDoubleClicked.connect(self.detail_person_page)

    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle('مشتریان')

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
            add_bookmark_page.update_person_combo()
            add_board_page.update_person_combo()
    
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
        self.cancel_edit_btn.clicked.connect(lambda :go_to_page(settings_page))

    def settings(self):
        """ Settings """
        self.setFixedSize(332,145)
        self.setWindowTitle(f'فرم: {self.form.title}')
    
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
            add_bookmark_page.update_form_combo()
            go_to_page(settings_page)


class ColorWidget(QWidget):
    
    def __init__(self, color: Color) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/color_widget.ui', self)
        self.color = color
        self.settings()
        self.init_ui()

        # Signals
        self.edit_btn.clicked.connect(self.edit_color)
        self.cancel_edit_btn.clicked.connect(lambda: go_to_page(settings_page))
    
    def settings(self):
        """ Settings """
        self.setFixedSize(332,145)
        self.setWindowTitle(f'رنگ: {self.color.color}')
    
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
            add_bookmark_page.update_color_combo()
            go_to_page(settings_page)


class SettingsPage(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/settings.ui', self)
        self.init_form_ui()
        self.init_color_ui()
        self.settings()

        # Signals
        self.home_btn.clicked.connect(lambda :go_to_page(home_page))
        self.close_btn.clicked.connect(close_app)
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
        self.setWindowTitle('تنظیمات')
    
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
            add_bookmark_page.update_form_combo()

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
        add_bookmark_page.update_form_combo()
    
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
            add_bookmark_page.update_color_combo()

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
        add_bookmark_page.update_color_combo()

    def edit_color_widget(self):
        """ Edit color widget """
        color_id = self.color_table.item(self.color_table.currentRow(), 0).text()
        color = query.query_color_by_id(session, color_id)
        color_widget = ColorWidget(color)
        stacked_layout.addWidget(color_widget)
        stacked_layout.setCurrentWidget(color_widget)


class OrderPage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/order.ui', self)
        self.settings()
        self.init_bookmark_ui()
        self.init_board_ui()

        # Signals
        self.close_btn.clicked.connect(close_app)
        self.home_btn.clicked.connect(lambda :go_to_page(home_page))
        self.add_bookmark_btn.clicked.connect(lambda :go_to_page(add_bookmark_page))
        self.delete_bookmark_btn.clicked.connect(self.delete_bookmark)
        self.cancel_bookmark_btn.clicked.connect(self.init_bookmark_ui)
        self.bookmark_list.itemClicked.connect(self.going_to_delete_bookmark)
        self.bookmark_list.itemDoubleClicked.connect(self.edit_bookmark_widget)

        self.add_board_btn.clicked.connect(lambda: go_to_page(add_board_page))
        self.delete_board_btn.clicked.connect(self.delete_board)
        self.cancel_board_btn.clicked.connect(self.init_board_ui)
        self.board_list.itemClicked.connect(self.going_to_delete_board)
        self.board_list.itemDoubleClicked.connect(self.edit_board_widget)
    
    def settings(self):
        """ Settings """
        self.setFixedSize(1000,600)
        self.setWindowTitle('سفارشات')

    def init_bookmark_ui(self):
        """ Initialize Bookmark UI """ 
        self.update_bookmark_list()
        self.delete_bookmark_btn.setEnabled(False)
        self.cancel_bookmark_btn.setEnabled(False)
    
    def update_bookmark_list(self):
        """ Update bookmark list """
        self.bookmark_list.setRowCount(0)
        bookmarks = query.query_all_bookmark(session)
        row_count = self.bookmark_list.rowCount()
        for bookmark in bookmarks:
            self.bookmark_list.insertRow(row_count)
            item_id = QTableWidgetItem(str(bookmark.id))
            item_id.setFlags(Qt.ItemIsEnabled)
            self.bookmark_list.setItem(row_count, 0, item_id)
            self.bookmark_list.setItem(row_count, 1, QTableWidgetItem(utils.get_full_name_person(bookmark.person)))
            self.bookmark_list.setItem(row_count, 2, QTableWidgetItem(str(bookmark.count)))
            self.bookmark_list.setItem(row_count, 3, QTableWidgetItem(bookmark.form.title))
            self.bookmark_list.setItem(row_count, 4, QTableWidgetItem(utils.get_colors(bookmark.colors)))
            self.bookmark_list.setItem(row_count, 5, QTableWidgetItem(utils.get_price(bookmark.final_price)))
            self.bookmark_list.setItem(row_count, 6, QTableWidgetItem(bookmark.zip_code))
            self.bookmark_list.setItem(row_count, 7, QTableWidgetItem(utils.get_date(bookmark.delivery_date)))
            self.bookmark_list.setItem(row_count, 8, QTableWidgetItem(utils.get_date(bookmark.created_date)))
            self.bookmark_list.setItem(row_count, 9, QTableWidgetItem(utils.get_date(bookmark.date_paid)))
            self.bookmark_list.setItem(row_count, 10, QTableWidgetItem(utils.get_status_payment(bookmark.is_paid)))
            row_count += 1

    def delete_bookmark(self):
        """ Deleting bookmark """
        bookmark_id = self.bookmark_list.item(self.bookmark_list.currentRow(), 0).text()
        utils.delete_bookmark(session, bookmark_id)
        self.init_bookmark_ui()
    
    def going_to_delete_bookmark(self):
        """ Going to delete bookmark """
        self.delete_bookmark_btn.setEnabled(True)        
        self.cancel_bookmark_btn.setEnabled(True)
    
    def edit_bookmark_widget(self):
        """ Edit bookmark widget """
        bookmark_id = self.bookmark_list.item(self.bookmark_list.currentRow(), 0).text()
        bookmark = query.query_bookmark_by_id(session, bookmark_id)
        bookmark_widget = BookmarkWidget(bookmark)
        stacked_layout.addWidget(bookmark_widget)
        stacked_layout.setCurrentWidget(bookmark_widget)

    def init_board_ui(self):
        """ Initialize Board UI """ 
        self.update_board_list()
        self.delete_board_btn.setEnabled(False)
        self.cancel_board_btn.setEnabled(False)
    
    def update_board_list(self):
        """ Update board list (table) """
        self.board_list.setRowCount(0)
        boards = query.query_all_board(session)
        row_count = self.board_list.rowCount()
        for board in boards:
            self.board_list.insertRow(row_count)
            item_id = QTableWidgetItem(str(board.id))
            item_id.setFlags(Qt.ItemIsEnabled)
            self.board_list.setItem(row_count, 0, item_id)
            self.board_list.setItem(row_count, 1, QTableWidgetItem(utils.get_full_name_person(board.person)))
            self.board_list.setItem(row_count, 2, QTableWidgetItem(str(board.count)))
            self.board_list.setItem(row_count, 3, QTableWidgetItem(utils.get_size_board(board)))
            self.board_list.setItem(row_count, 4, QTableWidgetItem(utils.get_time_board(board.time)))
            self.board_list.setItem(row_count, 5, QTableWidgetItem(utils.get_price(board.final_price)))
            self.board_list.setItem(row_count, 6, QTableWidgetItem(utils.get_has_logo_board(board.has_logo)))
            self.board_list.setItem(row_count, 7, QTableWidgetItem(utils.get_price(board.logo_price)))
            self.board_list.setItem(row_count, 8, QTableWidgetItem(utils.get_has_panel_board(board.has_panel)))
            self.board_list.setItem(row_count, 9, QTableWidgetItem(utils.get_price(board.panel_price)))
            self.board_list.setItem(row_count, 10, QTableWidgetItem(board.zip_code))
            self.board_list.setItem(row_count, 11, QTableWidgetItem(utils.get_status_payment(board.is_paid)))
            self.board_list.setItem(row_count, 12, QTableWidgetItem(utils.get_date(board.created_date)))
            self.board_list.setItem(row_count, 13, QTableWidgetItem(utils.get_date(board.delivery_date)))
            self.board_list.setItem(row_count, 14, QTableWidgetItem(utils.get_date(board.date_paid)))
            row_count += 1

    def delete_board(self):
        """ Deleting board """
        board_id = self.board_list.item(self.board_list.currentRow(), 0).text()
        utils.delete_board(session, board_id)
        self.init_board_ui()

    def going_to_delete_board(self):
        """ Going to delete board """
        self.delete_board_btn.setEnabled(True)        
        self.cancel_board_btn.setEnabled(True)

    def edit_board_widget(self):
        """ Edit board widget """
        board_id = self.board_list.item(self.board_list.currentRow(), 0).text()
        board = query.query_board_by_id(session, board_id)
        board_widget = BoardWidget(board)
        stacked_layout.addWidget(board_widget)
        stacked_layout.setCurrentWidget(board_widget)


class AddBookmarkPage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/add_bookmark.ui', self)
        self.settings()
        self.init_ui()

        # Signals
        self.add_btn.clicked.connect(self.add_bookmark)
        self.cancel_btn.clicked.connect(lambda :go_to_page(order_page))
        self.form_input.currentIndexChanged.connect(self.calculate_final_price)
        self.count_input.valueChanged.connect(self.calculate_final_price)
    
    def settings(self):
        """ Settings """
        self.setFixedSize(1000,500)
        self.setWindowTitle('سفارش بوکمارک')
    
    def init_ui(self):
        """ Initialize UI """
        self.update_person_combo()
        self.update_form_combo()
        self.update_color_combo()
        self.calculate_final_price()
        self.set_current_date()

    def update_person_combo(self):
        """ Update person combo """
        self.person_input.clear()
        perons = query.query_all_person(session)
        for person in perons:
            self.person_input.addItem(utils.get_full_name_person(person), userData=person.person_id)

    def update_form_combo(self):
        """ Update form combo """
        self.form_input.clear()
        forms = query.query_all_form(session)
        for form in forms:
            self.form_input.addItem(form.title, userData=form.id)

    def update_color_combo(self):
        """ Update color combo """
        self.colors_input.clear()
        colors = query.query_all_color(session)
        for color in colors:
            item = QListWidgetItem(color.color)
            item.setData(Qt.UserRole, color)
            self.colors_input.addItem(item)

    def calculate_final_price(self, value=None):
        """ Calculate final price """
        form_id = self.form_input.currentData()
        count = self.count_input.value()
        final_price = utils.calculate_final_price_bookmark(session, form_id, count)
        self.final_price_input.setValue(int(final_price))
    
    def set_current_date(self):
        """ Set current date """
        date = QDate.currentDate()
        self.created_date_input.setSelectedDate(date)

    def add_bookmark(self):
        """ Add a new bookmark """
        person_id = self.person_input.currentData()
        form_id = self.form_input.currentData()
        colors = self.colors_input.selectedItems()
        colors = [color.data(Qt.UserRole) for color in colors]
        count = self.count_input.value()
        final_price = 0
        final_price = self.final_price_input.value()
        is_paid = self.is_paid_input.isChecked() 
        created_date = self.created_date_input.selectedDate().toPyDate()
        adderess = self.adderess_input.toPlainText()
        zip_code = self.zip_code_input.text()
        data = {
            'person_id': person_id,
            'form_id': form_id,
            'colors': colors,
            'count': count,
            'final_price':final_price,
            'is_paid': is_paid,
            'created_date': created_date,
            'zip_code': zip_code.strip(),
            'adderess': adderess.strip(),
            'date_paid': None,
            'delivery_date': None,
        }
        is_valid = validete_form(data, non_required=['is_paid', 'date_paid', 'delivery_date'])
        if is_valid:
            utils.add_bookmark(session, **data)
            self.person_input.setCurrentIndex(0)
            self.form_input.setCurrentIndex(0)
            self.colors_input.clearSelection()
            self.count_input.setValue(1)
            self.final_price_input.setValue(0)
            self.is_paid_input.setChecked(False)
            self.set_current_date()
            self.adderess_input.clear()
            self.zip_code_input.clear()
            order_page.update_bookmark_list()
            go_to_page(order_page)


class BookmarkWidget(QWidget):

    def __init__(self, bookmark: Bookmark) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/edit_bookmark.ui', self)
        self.bookmark = bookmark
        self.settings()
        self.init_ui()

        # Signals
        self.edit_btn.clicked.connect(self.edit_bookmark)
        self.cancel_btn.clicked.connect(lambda :go_to_page(order_page))
        self.form_input.currentIndexChanged.connect(self.calculate_final_price)
        self.count_input.valueChanged.connect(self.calculate_final_price)
    
    def settings(self):
        """ Settings """
        self.setFixedSize(800,500)
        self.setWindowTitle('بوکمارک {}'.format(utils.get_full_name_person(self.bookmark.person)))
    
    def init_ui(self):
        """ Initialize UI """
        self.update_person_combo()
        self.update_form_combo()
        self.update_color_combo()
        # Set the current values
        self.person_input.setCurrentIndex(self.person_input.findData(self.bookmark.person_id))
        self.form_input.setCurrentIndex(self.form_input.findData(self.bookmark.form_id))
        
        # Set the colors
        for color in self.bookmark.colors:
            color_item = self.colors_input.findItems(color.color, Qt.MatchExactly)
            color_item[0].setSelected(True)
        
        self.count_input.setValue(self.bookmark.count)
        self.calculate_final_price() # set the final price
        self.is_paid_input.setChecked(self.bookmark.is_paid)
        self.adderess_input.setPlainText(self.bookmark.adderess)
        self.zip_code_input.setText(self.bookmark.zip_code)
        self.created_date_input.setSelectedDate(self.bookmark.created_date)
        self.date_paid_input.setDate(self.bookmark.date_paid or QDate())
        self.delivery_date_input.setDate(self.bookmark.delivery_date or QDate())

    def calculate_final_price(self, value=None):
        """ Calculate final price """
        form_id = self.form_input.currentData()
        count = self.count_input.value()
        final_price = utils.calculate_final_price_bookmark(session, form_id, count)
        self.final_price_input.setValue(final_price)
    
    def update_person_combo(self):
        """ Update person combo """
        self.person_input.clear()
        perons = query.query_all_person(session)
        for person in perons:
            self.person_input.addItem(utils.get_full_name_person(person), userData=person.person_id)

    def update_form_combo(self):
        """ Update form combo """
        self.form_input.clear()
        forms = query.query_all_form(session)
        for form in forms:
            self.form_input.addItem(form.title, userData=form.id)

    def update_color_combo(self):
        """ Update color combo """
        self.colors_input.clear()
        colors = query.query_all_color(session)
        for color in colors:
            item = QListWidgetItem(color.color)
            item.setData(Qt.UserRole, color)
            self.colors_input.addItem(item)

    def edit_bookmark(self):
        """ Edit bookmark """
        person_id = self.person_input.currentData()
        form_id = self.form_input.currentData()
        colors = self.colors_input.selectedItems()
        colors = [color.data(Qt.UserRole) for color in colors]
        count = self.count_input.value()
        final_price = 0
        final_price = self.final_price_input.value()
        is_paid = self.is_paid_input.isChecked() 
        created_date = self.created_date_input.selectedDate().toPyDate()
        date_paid = self.date_paid_input.date().toPyDate()
        delivery_date = self.delivery_date_input.date().toPyDate()
        adderess = self.adderess_input.toPlainText()
        zip_code = self.zip_code_input.text()
        data = {
            'person_id': person_id,
            'form_id': form_id,
            'colors': colors,
            'count': count,
            'final_price':final_price,
            'is_paid': is_paid,
            'created_date': created_date,
            'zip_code': zip_code.strip(),
            'adderess': adderess.strip(),
            'date_paid': date_paid,
            'delivery_date': delivery_date,
        }
        is_valid = validete_form(data, non_required=['is_paid'])
        if is_valid:
            utils.edit_bookmark(session, self.bookmark.id, **data)
            order_page.update_bookmark_list()
            go_to_page(order_page)


class AddBoardPage(QWidget):

    def __init__(self) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/add_board.ui', self)
        self.settings()
        self.init_ui()

    def settings(self):
        """ Settings """
        self.setFixedSize(1000,500)
        self.setWindowTitle('سفارش تابلو')

        # Signals
        self.add_btn.clicked.connect(self.add_board)
        self.cancel_btn.clicked.connect(lambda :go_to_page(order_page))
        self.has_logo_input.stateChanged.connect(self.toggle_logo_input)
        self.has_panel_input.stateChanged.connect(self.toggle_panel_input)
        self.time_input.timeChanged.connect(self.calculate_final_price)
        self.base_time_price_input.valueChanged.connect(self.calculate_final_price)
        self.count_input.valueChanged.connect(self.calculate_final_price)
        self.logo_price_input.valueChanged.connect(self.calculate_final_price)
        self.panel_price_input.valueChanged.connect(self.calculate_final_price)
    
    def init_ui(self):
        """ Initialize UI """
        self.update_person_combo()
        self.calculate_final_price()
        self.logo_price_input.setEnabled(False)
        self.panel_price_input.setEnabled(False)
    
    def update_person_combo(self):
        """ Update person combo """
        self.person_input.clear()
        perons = query.query_all_person(session)
        for person in perons:
            self.person_input.addItem(utils.get_full_name_person(person), userData=person.person_id)

    def toggle_logo_input(self, state):
        """ Toggle logo input """
        if state == Qt.Checked:
            self.logo_price_input.setEnabled(True)
        else:
            self.logo_price_input.setValue(0)
            self.logo_price_input.setEnabled(False)
        
    def toggle_panel_input(self, state):
        """ Toggle panel input """
        if state == Qt.Checked:
            self.panel_price_input.setEnabled(True)
        else:
            self.panel_price_input.setValue(0)
            self.panel_price_input.setEnabled(False)

    def calculate_final_price(self):
        """ Calculate final price """
        time = self.time_input.time().toPyTime().hour
        base_time_price = self.base_time_price_input.value()
        count = self.count_input.value()
        final_price = time * base_time_price * count
        has_logo = self.has_logo_input.isChecked()
        if has_logo:
            logo_price = self.logo_price_input.value()
            final_price += logo_price
        has_panel = self.has_panel_input.isChecked()
        if has_panel:
            panel_price = self.panel_price_input.value()
            final_price += panel_price
        
        self.final_price_input.setValue(final_price)
    
    def add_board(self):
        """ Add Board """
        person_id = self.person_input.currentData()
        width = self.width_size_input.value()
        height = self.height_size_input.value()
        count = self.count_input.value()
        time = self.time_input.time().toPyTime()
        base_time_price = self.base_time_price_input.value()
        final_price = self.final_price_input.value()
        has_logo = self.has_logo_input.isChecked()
        has_panel = self.has_panel_input.isChecked()
        logo_price = self.logo_price_input.value()
        panel_price = self.panel_price_input.value()
        adderess = self.adderess_input.toPlainText()
        zip_code = self.zip_code_input.text()
        description = self.description_input.toPlainText()
        created_date = self.created_date_input.selectedDate().toPyDate()
        is_paid = False
        date_paid = None
        delivery_date = None
        data = {
            'person_id': person_id,
            'width_size': width,
            'height_size': height,
            'count': count,
            'time': time,
            'base_time_price': base_time_price,
            'final_price': final_price,
            'has_logo': has_logo,
            'has_panel': has_panel,
            'logo_price': logo_price,
            'panel_price': panel_price,
            'adderess': adderess.strip(),
            'zip_code': zip_code.strip(),
            'description': description.strip(),
            'created_date': created_date,
            'is_paid': is_paid,
            'date_paid': date_paid,
            'delivery_date': delivery_date,
        }
        non_required = ['is_paid', 'date_paid', 'delivery_date', 'description', 'has_logo', 'has_panel']
        if not has_logo:
            non_required.append('logo_price')
        if not has_panel:
            non_required.append('panel_price')

        is_valid = validete_form(data, non_required=non_required)
        if is_valid:
            utils.add_board(session, **data)
            order_page.update_board_list()
            go_to_page(order_page)


class BoardWidget(QWidget):

    def __init__(self, board: Board) -> None:
        super().__init__()
        loadUi(APP_DIR / 'ui/board_widget.ui', self)
        self.board = board
        self.settings()
        self.init_ui()

        # Signals
        self.cancel_btn.clicked.connect(lambda :go_to_page(order_page))
        self.edit_btn.clicked.connect(self.edit_board)
        self.has_logo_input.stateChanged.connect(self.toggle_logo_input)
        self.has_panel_input.stateChanged.connect(self.toggle_panel_input)
        self.time_input.timeChanged.connect(self.calculate_final_price)
        self.base_time_price_input.valueChanged.connect(self.calculate_final_price)
        self.count_input.valueChanged.connect(self.calculate_final_price)
        self.logo_price_input.valueChanged.connect(self.calculate_final_price)
        self.panel_price_input.valueChanged.connect(self.calculate_final_price)

    def settings(self):
        """ Settings """
        self.setFixedSize(1000,500)
        self.setWindowTitle('تابلو {}'.format(utils.get_full_name_person(self.board.person)))
    
    def init_ui(self):
        """ Initializer UI """
        self.update_person_combo()
        if not self.board.has_logo:
            self.logo_price_input.setEnabled(False)
        else:
            self.logo_price_input.setEnabled(True)

        if not self.board.has_panel:
            self.panel_price_input.setEnabled(False)
        else:
            self.panel_price_input.setEnabled(True)

        self.person_input.setCurrentIndex(self.person_input.findData(self.board.person_id))
        self.width_size_input.setValue(self.board.width_size)
        self.height_size_input.setValue(self.board.height_size)
        self.count_input.setValue(self.board.count)
        self.time_input.setTime(QTime(self.board.time.hour, self.board.time.minute))
        self.base_time_price_input.setValue(int(self.board.base_time_price))
        self.final_price_input.setValue(int(self.board.final_price))
        self.has_logo_input.setChecked(self.board.has_logo)
        self.has_panel_input.setChecked(self.board.has_panel)
        self.logo_price_input.setValue(int(self.board.logo_price))
        self.panel_price_input.setValue(int(self.board.panel_price))
        self.adderess_input.setPlainText(self.board.adderess)
        self.zip_code_input.setText(self.board.zip_code)
        self.description_input.setPlainText(self.board.description)
        self.created_date_input.setSelectedDate(self.board.created_date)
        self.is_paid_input.setChecked(self.board.is_paid)
        if self.board.date_paid:
            self.date_paid_input.setDate(self.board.date_paid)
        if self.board.delivery_date:
            self.delivery_date_input.setDate(self.board.delivery_date)

    def update_person_combo(self):
        """ Update person combo """
        self.person_input.clear()
        perons = query.query_all_person(session)
        for person in perons:
            self.person_input.addItem(utils.get_full_name_person(person), userData=person.person_id)

    def edit_board(self):
        """ Edit board """
        person_id = self.person_input.currentData()
        width = self.width_size_input.value()
        height = self.height_size_input.value()
        count = self.count_input.value()
        time = self.time_input.time().toPyTime()
        base_time_price = self.base_time_price_input.value()
        final_price = self.final_price_input.value()
        has_logo = self.has_logo_input.isChecked()
        has_panel = self.has_panel_input.isChecked()
        logo_price = self.logo_price_input.value()
        panel_price = self.panel_price_input.value()
        adderess = self.adderess_input.toPlainText()
        zip_code = self.zip_code_input.text()
        description = self.description_input.toPlainText()
        created_date = self.created_date_input.selectedDate().toPyDate()
        is_paid = self.is_paid_input.isChecked()
        date_paid = self.date_paid_input.date().toPyDate()
        delivery_date = self.delivery_date_input.date().toPyDate()
        data = {
            'person_id': person_id,
            'width_size': width,
            'height_size': height,
            'count': count,
            'time': time,
            'base_time_price': base_time_price,
            'final_price': final_price,
            'has_logo': has_logo,
            'has_panel': has_panel,
            'logo_price': logo_price,
            'panel_price': panel_price,
            'adderess': adderess.strip(),
            'zip_code': zip_code.strip(),
            'description': description.strip(),
            'created_date': created_date,
            'is_paid': is_paid,
            'date_paid': date_paid,
            'delivery_date': delivery_date,
        }
        non_required = ['is_paid', 'has_logo', 'has_panel', 'description']
        if not has_logo:
            non_required.append('logo_price')
        if not has_panel:
            non_required.append('panel_price')

        is_valid = validete_form(data, non_required=non_required)
        if is_valid:
            utils.edit_board(session, self.board.id, **data)
            order_page.update_board_list()
            go_to_page(order_page)

    def toggle_logo_input(self, state):
        """ Toggle logo input """
        if state == Qt.Checked:
            self.logo_price_input.setEnabled(True)
            self.logo_price_input.setValue(int(self.board.logo_price))

        else:
            self.logo_price_input.setValue(0)
            self.logo_price_input.setEnabled(False)
        
    def toggle_panel_input(self, state):
        """ Toggle panel input """
        if state == Qt.Checked:
            self.panel_price_input.setEnabled(True)
            self.panel_price_input.setValue(int(self.board.panel_price))
        else:
            self.panel_price_input.setValue(0)
            self.panel_price_input.setEnabled(False)

    def calculate_final_price(self):
        """ Calculate final price """
        time = self.time_input.time().toPyTime().hour
        base_time_price = self.base_time_price_input.value()
        count = self.count_input.value()
        final_price = time * base_time_price * count
        has_logo = self.has_logo_input.isChecked()
        if has_logo:
            logo_price = self.logo_price_input.value()
            final_price += logo_price
        has_panel = self.has_panel_input.isChecked()
        if has_panel:
            panel_price = self.panel_price_input.value()
            final_price += panel_price
        
        self.final_price_input.setValue(final_price)

### End Pages ###


### Run ###

if __name__ == '__main__':
    app = QApplication(sys.argv)

    home_page = HomePage()
    person_page = PersonPage()
    settings_page = SettingsPage()
    order_page = OrderPage()
    add_bookmark_page = AddBookmarkPage()
    add_board_page = AddBoardPage()

    stacked_layout = QStackedLayout()
    stacked_layout.addWidget(home_page)
    stacked_layout.addWidget(person_page)
    stacked_layout.addWidget(settings_page)
    stacked_layout.addWidget(order_page)
    stacked_layout.addWidget(add_bookmark_page)
    stacked_layout.addWidget(add_board_page)

    app.exec()

### End Run ###

