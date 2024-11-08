'''
Defining the models:
 - User
 - Product
 - Category
'''

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# creating user model
class User(Base):
    __tablename__ = 'users' # setting table name in the database
    # creating columns in the table, id, username and hashed_password
    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# creating category model
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# product model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id')) # connecting this column (and table) to categories table and id column through foreign key
    category = relationship('Category') # creating relationship with Category table