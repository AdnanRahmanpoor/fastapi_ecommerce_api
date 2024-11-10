'''
Creating CRUD operations and routes + search and filters
'''
# APIRouter helps in organizing routes and creating reusable code | Depends injects dependencies into route function
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
# SQLALCHEMY session for interaction with database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# importing schemas for creation of products and getting info about them
from .schemas import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate
# importing get_db function so session can interact with a database
from .database import get_db
# importing product model
from .models import Category, Product

# creating apirouter instance
product_router = APIRouter()
category_router = APIRouter()
# Creating a product 
# POST method using the APIRouter and setting the route to /products
@product_router.post('/products', response_model=ProductResponse)
# create func and takes product as parameter and sets its format to ProductCreate as defined in Schemas.py, db session uses depends to inject into a get_db func
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = Product(**product.dict()) # unpacking product dict and creating a Product instance
    db.add(db_product) # adding the product instance to a database session
    await db.commit() # commiting the changes to the database (saving)
    await db.refresh(db_product) # refreshing the instance and assigning an 'id' to each db_product
    return db_product # returning the created product which FastAPI searializes to ProductResponse

# Reading a Product
# GET method to retrieve information about a product using product_id, using ProductResponse 
@product_router.get('/products/{product_id}', response_model=ProductResponse)
# function for getting product info using product id and the Session to get from the database
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # return a database query which looks in Product table and get the first item that matches the product id
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Updating a product
# PUT method which will update a product based on product id
@product_router.put('/products/{product_id}', response_model=ProductResponse)
# func to update a product based on product id
async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    # query to get a product based on product id
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalars().first()

    # if the product is not available throw an 404 error
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # if the product is available then update the fields which were specified in the request
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.add(db_product) # ensure updated product is added back to the database
    await db.commit() # commit changes to the database
    await db.refresh(db_product) # refresh database 
    return db_product # return the updated product

# Delete a product
# DELETE method using productrouter to delete a product based on product_id, and uses 204 https response code for successful deletion
@product_router.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
# func which selects a product based on product_id and deletes it
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # querying a product from the database which matches the product_id
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalars().first()

    # if the product doesnt exist throw a 404 not found error
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    # if the product exists
    await db.delete(db_product) # delete the product 
    await db.commit() # commit changes to the database
    return

# Search and Filter products
# using GET method to retrieve products, the response will be List of products
@product_router.get('/products', response_model=List[ProductResponse])
# func to get products with optional price and category parameters
async def get_products(price: Optional[float] = None, category_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    # query the to get all products from the Product table
    query = select(Product)

    # checking if price parameter was provided 
    if price:
        # getting the product with price equal to or less than specified
        query = query.where(Product.price <= price)
    # checking if category parameter was provided
    if category_id:
        # filtering the products to get the category_id that was specified
        query = query.where(Product.category_id == category_id)
    # return all products based on the query
    result = await db.execute(query)
    return result.scalars().all()

@category_router.post('/category', response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@category_router.get('/category/{category_id}', response_model=CategoryResponse)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalars().first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category