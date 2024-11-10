'''
Main FastAPI
'''

# importing libraries and functions
from fastapi import FastAPI
from .database import init_db
from .auth import auth_router
from .crud import product_router, category_router

# initializing FastAPI with a title
app = FastAPI(title="E-commerce Product Catalog API")

# on app startup run init_db()
@app.on_event('startup')
async def startup():
    await init_db()

# include the following routers to the app
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)