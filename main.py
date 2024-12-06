from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],  # Specify the allowed origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Redis connection setup
redis = get_redis_connection(
  host='redis-12486.c265.us-east-1-2.ec2.redns.redis-cloud.com',
  port=12486,
  password='2g9Rv9vZwdsdlzYozAX72EqcPye0nQCH')


# Define the Product model
class Product(HashModel):
    name: str
    price: float
    quantity: int
    class Meta:
        database = redis  # Connect this model to the Redis database

# Define a Pydantic model for creating a product (optional, but recommended)
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/products")
def all_products():
    product_pks = Product.all_pks()  # This returns a list of primary keys (IDs)
    products = [Product.get(pk) for pk in product_pks]
    return [product.dict() for product in products]  

@app.post('/product')
def create_product(product: ProductCreate):
    new_product = Product(**product.dict())  # Convert the input data to the Product model
    new_product.save()
    return {"message": "Product created successfully", "product": new_product.dict()}

@app.get('/product/{pk}')
def product_fetch(pk:str):
    return Product.get(pk)

@app.delete('/product/{pk}')
def delete_product(pk:str):
    return Product.delete(pk)
