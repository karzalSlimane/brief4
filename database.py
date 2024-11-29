
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def setup_database():
    engine = create_engine('postgresql://postgres:karzal@localhost:3000/immo_db')  
    Session = sessionmaker(bind=engine)
    return Session
