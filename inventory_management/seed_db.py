from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import os

# Define the database URL
# export DATABASE_URL="postgresql://postgres:postgres@192.168.86.53:5432/marketdb"

# Create an engine that stores data in the local directory's supermarket_inventory.db file
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

# Declare a base for our class definitions
Base = declarative_base()


# Define a class that maps to a table in the database
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    supplier = Column(String(100), nullable=False)

    def __repr__(self):
        return (f"<Product(id='{self.id}', name='{self.name}', category='{self.category}', "
                f"quantity='{self.quantity}', price='{self.price}', supplier='{self.supplier}')>")


# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Faker instance
fake = Faker()

# List of possible categories and suppliers
categories = ['Fruit', 'Vegetable', 'Dairy', 'Bakery', 'Meat', 'Seafood', 'Beverage', 'Snack']
suppliers = ['Fresh Farms', 'Organic Valley', 'Best Bakery', 'Meat Masters', 'Ocean Harvest', 'Drink Delight']


# Generate random products
def generate_random_product():
    return Product(
        name=fake.word().capitalize(),
        category=random.choice(categories),
        quantity=random.randint(10, 200),
        price=round(random.uniform(0.5, 20.0), 2),
        supplier=random.choice(suppliers)
    )


# Add generated products to the session and commit
def add_products_to_db(session, num_products=50):
    for _ in range(num_products):
        session.add(generate_random_product())
    session.commit()


# Create a Session
session = Session()

# Add random products to the database
add_products_to_db(session, num_products=50)

# Query the database to verify
for product in session.query(Product).all():
    print(product)

# Close the session
session.close()
