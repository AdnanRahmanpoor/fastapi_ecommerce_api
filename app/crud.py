'''
Creating CRUD operations and routes + search and filters
'''
# APIRouter helps in organizing routes and creating reusable code | Depends injects dependencies into route function
from fastapi import APIRouter, Depends
# SQLALCHEMY session for interaction with database
from sqlalchemy.orm import Session
# importing schemas for creation of products and getting info about them
from .schemas import ProductCreate, ProductResponse
# importing init_db function so session can interact with a database
from .database import init_db
# importing product model
from .models import Product

# creating apirouter instance
product_router = APIRouter()

# Creating a product 
# POST method using the APIRouter and setting the route to /products
@product_router.post('/products', response_model=ProductResponse)
# create func and takes product as parameter and sets its format to ProductCreate as defined in Schemas.py, db session uses depends to inject into a init_db func
async def create_product(product: ProductCreate, db: Session = Depends(init_db)):
    db_product = Product(**product.dict()) # unpacking product dict and creating a Product instance
    db.add(db_product) # adding the product instance to a database session
    db.commit() # commiting the changes to the database (saving)
    db.refresh(db_product) # refreshing the instance and assigning an 'id' to each db_product
    return db_product # returning the created product which FastAPI searializes to ProductResponse

# Reading a Product
# GET method to retrieve information about a product using product_id, using ProductResponse 
@product_router.get('/products/{product_id}', response_model=ProductResponse)
# function for getting product info using product id and the Session to get from the database
async def read_product(product_id: int, db: Session = Depends(init_db)):
    # return a database query which looks in Product table and get the first item that matches the product id
    return db.query(Product).filter(Product.id == product_id).first()

# 