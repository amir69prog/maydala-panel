#!/usr/bin/python3

""" 
    Utils: 
        Like:
            adding board,
            adding bookmark,
            adding color,
            adding form,
            adding person

"""

from datetime import datetime
from typing import List

from core.models import *

def get_full_name_person(person: Person) -> str:
    """ Get the Fullname of person """
    return f'{person.first_name} {person.last_name}'

def get_status_payment(is_paid: bool) -> str:
    """ Get status of payment bookmark/board """
    if is_paid:
        return 'پرداخت شده'
    return 'پرداخت نشده'

def get_date(date: datetime) -> str:
    """ Return normal format of date if that exists. otherwise return dashes """
    if not date:
        return '-----'
    return date.strftime('%Y-%m-%d')

def get_colors(colors: List) -> str:
    """ Return better template for colors items """
    
    if colors:
        return ', '.join([color.color for color in colors])
    return '-----'

def calculate_final_price_bookmark(session, form_id, count) -> float:
    """ Calculate final price of bookmark """
    form = session.query(Form).filter(Form.id == form_id).first()
    if form:
        return form.base_price * count
    return 0.0

### Add ###

def add_person(session, *args, **kwargs):
    """Inserting Person object
       this function return the person that has been created"""
    
    first_person = Person(**kwargs)
    session.add(first_person)
    session.commit()
    return first_person

def add_bookmark(session, *args, **kwargs):
    """Inserting Bookmark object
       this function return the bookmark that has been created"""
    
    first_bookmark = Bookmark(**kwargs)
    session.add(first_bookmark)
    session.commit()
    return first_bookmark

def add_color(session, *args, **kwargs):
    """Inserting Color object
       this function return the color that has been created"""
    
    first_color = Color(**kwargs)
    session.add(first_color)
    session.commit()
    return first_color

def add_form(session, *args, **kwargs):
    """Inserting Form object
       this function return the form that has been created"""
    
    first_form = Form(**kwargs)
    session.add(first_form)
    session.commit()
    return first_form

def add_board(session, *args, **kwargs):
    """Inserting Board object
       this function return the board that has been created"""
    
    first_board = Board(**kwargs)
    session.add(first_board)
    session.commit()
    return first_board

def append_color_to_bookmark(session, bookmark_id, color_id):
    """Append color to bookmark"""
    bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    color = session.query(Color).filter(Color.id == color_id).first()
    bookmark.colors.append(color)
    session.commit()

### End Add ###


### Edit ###

def edit_person(session, person_id, *args, **kwargs):
    """Edit person"""
    person = session.query(Person).filter(Person.person_id == person_id).first()
    person.first_name = kwargs['first_name']
    person.last_name = kwargs['last_name']
    person.phone_number = kwargs['phone_number']
    session.commit() 

def edit_form(session, form_id, *args, **kwargs):
    """Edit form"""
    form = session.query(Form).filter(Form.id == form_id).first()
    form.title = kwargs['title']
    form.base_price = kwargs['base_price']
    session.commit()

def edit_color(session, color_id, *args, **kwargs):
    """Edit color"""
    color = session.query(Color).filter(Color.id == color_id).first()
    color.color = kwargs['color']
    session.commit()


def edit_bookmark(session, bookmark_id, *args, **kwargs):
    """ Edit bookmark """
    bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    for key, value in kwargs.items():
        setattr(bookmark, key, value)
    session.commit()

### End Edit ###


### Delete ###

def delete_person(session, person_id):
    """Delete person"""
    person = session.query(Person).filter(Person.person_id == person_id).first()
    session.delete(person)
    session.commit()

def delete_form(session, form_id):
    """Delete form"""
    form = session.query(Form).filter(Form.id == form_id).first()
    session.delete(form)
    session.commit()

def delete_color(session, color_id):
    """Delete color"""
    color = session.query(Color).filter(Color.id == color_id).first()
    session.delete(color)
    session.commit()

def delete_bookmark(session, bookmark_id):
    """ Delete bookmark """
    bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    session.delete(bookmark)
    session.commit()

### End Delete ###