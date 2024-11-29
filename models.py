import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

# Database connection using a properly formatted URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:karzal@localhost:3000/immo_db")

engine = create_engine(DATABASE_URL)

# City Table
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship with Annonce (One-to-Many)
    annonces = relationship("Annonce", back_populates="city")

# Many-to-Many Association Table between Annonce and Equipment
annonce_equipment = Table(
    'annonce_equipment', Base.metadata,
    Column('annonce_id', Integer, ForeignKey('annonce.id'), primary_key=True),
    Column('equipment_id', Integer, ForeignKey('equipment.id'), primary_key=True)
)

# Equipment Table
class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship with Annonce through the association table (Many-to-Many)
    annonces = relationship("Annonce", secondary=annonce_equipment, back_populates="equipments")

# Annonce Table
class Annonce(Base):
    __tablename__ = 'annonce'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=True)  # Use Float for numeric price values
    datetime = Column(DateTime, nullable=False)
    nb_rooms = Column(Integer, nullable=True)
    nb_baths = Column(Integer, nullable=True)
    surface_area = Column(Float, nullable=True)
    link = Column(String, nullable=True)

    # Foreign Key to City Table
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    city = relationship("City", back_populates="annonces")

    # Relationship with Equipment through the association table (Many-to-Many)
    equipments = relationship("Equipment", secondary=annonce_equipment, back_populates="annonces")



