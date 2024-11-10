# E-commerce Product Catalog API using FastAPI

This is a RESTful API built with FastAPI for managing a catalog of products in an e-commerce application. It supports CRUD operations on products and categories, with features for user authentication, searching, filtering.

## Features

- **Product and Category CRUD Operations**: Create, read, update, and delete products and categories.
- **JWT-Based User Authentication**: Secure access to routes with JWT authentication.
- **Filtering and Searching**: Search for products by price or category.
- **PostgreSQL Database**: Integrated with PostgreSQL using SQLAlchemy.

## Technologies Used

- **FastAPI**: For creating the RESTful API.
- **PostgreSQL**: Relational database to store products and categories.
- **SQLAlchemy**: ORM for database interactions.
- **JWT**: Authentication using JSON Web Tokens.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/AdnanRahmanpoor/fastapi_ecommerce_api.git
    cd fastapi_ecommerce_api
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:  
   Create a `.env` file with the following configuration:
    ```env
    DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. **Initialize the Database**:
    ```bash
    python -m app.database init_db
    ```

## Usage

1. **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

2. **API Documentation**:  
   Once the server is running, access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Authentication

- **POST** `/auth/login` - Authenticate user and receive JWT token.

### Products

- **POST** `/products` - Create a new product.
- **GET** `/products/{product_id}` - Retrieve a product by ID.
- **PUT** `/products/{product_id}` - Update a product by ID.
- **DELETE** `/products/{product_id}` - Delete a product by ID.
- **GET** `/products` - Retrieve products with optional filters for price and category.

### Categories

- **POST** `/category` - Create a new category.
- **GET** `/category/{category_id}` - Retrieve a category by ID.

## Schemas

### Product
- **ProductCreate**: Schema for creating a product.
- **ProductResponse**: Schema for retrieving a product.
- **ProductUpdate**: Schema for updating a product.

### Category
- **CategoryCreate**: Schema for creating a category.
- **CategoryResponse**: Schema for retrieving a category.

## Example Requests

### Create a Product
```json
POST /products
{
    "name": "Sample Product",
    "description": "A sample product description.",
    "price": 29.99,
    "category_id": 1
}
```

### Filter Products by Price and Category
```http
GET /products?price=50&category_id=1
```

## Contributing

Feel free to submit pull requests or create issues for any bugs or feature requests.

## License

This project is licensed under the MIT License.