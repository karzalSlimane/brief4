from models import City, Equipment, Annonce, annonce_equipment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Database connection using a properly formatted URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:karzal@localhost:3000/immo_db")
engine = create_engine(DATABASE_URL)

# Create a session maker using the engine
Session = sessionmaker(bind=engine)
session = Session()

# Get available cities
def get_cities(session):
    cities = session.query(City.name).distinct().all()
    return [city[0] for city in cities]

# Get available equipment
def get_equipment(session):
    equipment = session.query(Equipment.name).distinct().all()
    return [equip[0] for equip in equipment]

# Function to retrieve filtered advertisements
def get_filtered_ads(session, price_min, price_max, rooms_min, rooms_max, bathrooms_min, bathrooms_max, city, equipment, start_date, end_date):
    query = session.query(
        Annonce.title,
        Annonce.price,
        Annonce.datetime,
        Annonce.nb_rooms,
        Annonce.nb_baths,
        Annonce.surface_area,
        Annonce.link,
        City.name.label('city'),
        Equipment.name.label('equipment')
    ).join(City).outerjoin(annonce_equipment).outerjoin(Equipment)

    # Add filters dynamically
    if price_min is not None and price_max is not None:
        query = query.filter(Annonce.price.between(price_min, price_max))
    if rooms_min is not None and rooms_max is not None:
        query = query.filter(Annonce.nb_rooms.between(rooms_min, rooms_max))
    if bathrooms_min is not None and bathrooms_max is not None:
        query = query.filter(Annonce.nb_baths.between(bathrooms_min, bathrooms_max))
    if city:
        query = query.filter(City.name == city)
    if equipment:
        query = query.filter(Equipment.name.in_(equipment))
    if start_date and end_date:
        query = query.filter(Annonce.datetime.between(start_date, end_date))

    # Use distinct to avoid duplicates due to the many-to-many relationship
    query = query.distinct()

    return query.all()
