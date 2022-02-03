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

from core.models import *

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

def edit_person(session, person_id, *args, **kwargs):
    """Edit person"""
    person = session.query(Person).filter(Person.person_id == person_id).first()
    person.first_name = kwargs['first_name']
    person.last_name = kwargs['last_name']
    person.phone_number = kwargs['phone_number']
    session.commit() 

def delete_person(session, person_id):
    """Delete person"""
    person = session.query(Person).filter(Person.person_id == person_id).first()
    session.delete(person)
    session.commit()