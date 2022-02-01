#!/usr/bin/python3

""" Queries for Tables """

from core.models import *
from typing import List

def query_all_person(session) -> List[Person]:
    """ Query for all person that created """
    query = session.query(Person).all()
    session.commit()
    return query