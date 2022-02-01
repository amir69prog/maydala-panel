from sqlalchemy.orm import sessionmaker
from core.models import engine

Session = sessionmaker(bind=engine)
session = Session()