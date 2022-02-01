from itertools import count
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

__all__ = [
    'Person',
]


Base = declarative_base()
engine = create_engine('sqlite:///core/database/database.db')


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    first_name = Column(String(255)) 
    last_name = Column(String(255))
    phone_number = Column(String(14))
    carts = relationship('Cart')

    def __repr__(self):
        return f"Person(name='{self.first_name} {self.last_name}' phone='{self.phone_number}')"


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, Sequence('cart_id_seq'), primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id')) 
    final_price = Column(Float)
    adderess = Column(Text) 
    zip_code = Column(String(10))
    is_paid = Column(Boolean, default=False)
    date_paid = Column(DateTime, nullable=True)
    products = relationship('Product')


class Product(Base):
    __tablename__ = 'product'
    # __abstract__ = True

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    count = Column(Integer)
    price = Column(Float)
    created_date = Column(DateTime)
    delivery_date = Column(DateTime, nullable=True) 


Base.metadata.create_all(engine)