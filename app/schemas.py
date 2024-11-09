from pydantic import BaseModel # validation and serialization of data for api
from typing import Optional

# data required to create User model: username and password and their type is string
class UserCreate(BaseModel):
    username: str
    password: str

# core attributes of a product
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

# inheriting from productbase to create a new product
class ProductCreate(ProductBase):
    pass

# this is for retreiving product data from productbase, and assigns an 'id' to each product response
class ProductResponse(ProductBase):
    id: int

# schema for updating products
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None