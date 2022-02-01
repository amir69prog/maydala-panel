#!/usr/bin/python3

""" 
    Utils: 
        Like:
            adding user,

"""

from core.models import *

def add_person(session, *args, **kwargs):
    """Inserting Person object
       this function return the person that has been created"""
    
    first_person = Person(**kwargs)
    session.add(first_person)
    session.commit()
    return first_person