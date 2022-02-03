#!/usr/bin/python3

""" Queries for Tables """

from typing import List

from core.models import *
from core.session import session

__all__ = [
    'query_all_person',
    'query_all_bookmark',
    'query_all_color',
    'query_all_form',
    'query_all_board',
    'query_person_by_id',
    'query_bookmark_by_id',
    'query_color_by_id',
    'query_form_by_id',
    'query_board_by_id',
]

def query_all_person(session) -> List[Person]:
    """ Query for all person that created """
    query = session.query(Person).all()
    session.commit()
    return query

def query_all_bookmark(session) -> List[Bookmark]:
    """ Query for all bookmark that created """
    query = session.query(Bookmark).all()
    session.commit()
    return query

def query_all_color(session) -> List[Color]:
    """ Query for all color that created """
    query = session.query(Color).all()
    session.commit()
    return query

def query_all_form(session) -> List[Form]:
    """ Query for all form that created """
    query = session.query(Form).all()
    session.commit()
    return query

def query_all_board(session) -> List[Board]:
    """ Query for all board that created """
    query = session.query(Board).all()
    session.commit()
    return query

def query_person_by_id(session, id) -> Person:
    """ Query for person by id """
    query = session.query(Person).filter(Person.person_id == id).first()
    session.commit()
    return query

def query_bookmark_by_id(session, id) -> Bookmark:
    """ Query for bookmark by id """
    query = session.query(Bookmark).filter(Bookmark.id == id).first()
    session.commit()
    return query

def query_color_by_id(session, id) -> Color:
    """ Query for color by id """
    query = session.query(Color).filter(Color.id == id).first()
    session.commit()
    return query

def query_form_by_id(session, id) -> Form:
    """ Query for form by id """
    query = session.query(Form).filter(Form.id == id).first()
    session.commit()
    return query

def query_board_by_id(session, id) -> Board:
    """ Query for board by id """
    query = session.query(Board).filter(Board.id == id).first()
    session.commit()
    return query
