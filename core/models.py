from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

__all__ = [
    'Person',
    'Form',
    'Color',
    'Bookmark',
    'Board',
]


Base = declarative_base()
engine = create_engine('sqlite:///core/database/database.db')

color_bookmark = Table('color_bookmark', Base.metadata,
    Column('bookmark_id', ForeignKey('bookmark.id')),
    Column('color_id', ForeignKey('color.id'))
)

class Form(Base):
    __tablename__ = 'form'

    id = Column(Integer, Sequence('form_id_seq'), primary_key=True)
    title = Column(String(100))
    base_price = Column(Float)
    bookmarks = relationship('Bookmark')

    def __repr__(self):
        return '<Form(id={}, title={}, base_price={})>'.format(self.id, self.title, self.base_price)

class Color(Base):
    __tablename__ = 'color'

    id = Column(Integer, Sequence('form_id_seq'), primary_key=True)
    color = Column(String(100))

    def __repr__(self):
        return f'<Color({self.color})>'


class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    first_name = Column(String(255)) 
    last_name = Column(String(255))
    phone_number = Column(String(14))
    bookmarks = relationship('Bookmark')
    boards = relationship('Board')
    
    def __repr__(self):
        return f"<Person(name={self.first_name} {self.last_name} phone={self.phone_number})>"


class Bookmark(Base):
    __tablename__ = 'bookmark'
    
    id = Column(Integer, Sequence('bookmark_id_seq'), primary_key=True)
    adderess = Column(Text) 
    zip_code = Column(String(10))
    is_paid = Column(Boolean, default=False)
    date_paid = Column(DateTime, nullable=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    person = relationship('Person', overlaps="bookmarks")
    count = Column(Integer)
    final_price = Column(Float)
    created_date = Column(DateTime)
    delivery_date = Column(DateTime, nullable=True)
    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship('Form', overlaps="bookmarks")
    colors = relationship('Color', secondary=color_bookmark)

    def __repr__(self) -> str:
        return f"<Bookmark(person_id={self.person_id}, count={self.count}, final_price={self.final_price})>"



class Board(Base):
    __tablename__ = 'board'
    
    id = Column(Integer, Sequence('bookmark_id_seq'), primary_key=True)
    adderess = Column(Text) 
    zip_code = Column(String(10))
    is_paid = Column(Boolean, default=False)
    date_paid = Column(DateTime, nullable=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    person = relationship('Person', overlaps="boards")
    count = Column(Integer)
    final_price = Column(Float)
    created_date = Column(DateTime)
    delivery_date = Column(DateTime, nullable=True)
    width_size = Column(Integer)
    height_size = Column(Integer)
    base_time_price = Column(Float, default=50.00)
    time = Column(Time)
    has_panel = Column(Boolean)
    has_logo = Column(Boolean)
    logo_price = Column(Float, default=0.00)
    panel_price = Column(Float, default=0.00)
    description = Column(Text)

    def __repr__(self) -> str:
        return f"<Board(cart_id={self.cart_id}, final_price={self.final_price} size={self.width_size}x{self.height_size})>"

if __name__ == '__main__':
    Base.metadata.create_all(engine)