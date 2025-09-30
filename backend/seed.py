from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models

# Create tables
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # Clear existing data
    db.query(models.Order).delete()
    db.query(models.Product).delete()
    db.commit()

    # --- Create Products ---
    products_to_add = [
        models.Product(
            name="iPhone 15 Pro",
            description="The latest and greatest iPhone with the A17 Pro chip.",
            price=999.99,
            stock=150,
            category="Electronics",
            specs={"color": "Titanium Blue", "storage": "256GB"},
        ),
        models.Product(
            name="MacBook Pro 14-inch",
            description="A powerful laptop for professionals with the M3 chip.",
            price=1999.00,
            stock=75,
            category="Electronics",
            specs={"chip": "M3 Pro", "ram": "18GB", "storage": "512GB SSD"},
        ),
        models.Product(
            name="Sony WH-1000XM5 Headphones",
            description="Industry-leading noise-canceling headphones.",
            price=399.00,
            stock=200,
            category="Accessories",
            specs={"color": "Black", "type": "Over-ear"},
        ),
        models.Product(
            name="Organic Cotton T-Shirt",
            description="A comfortable and stylish t-shirt made from 100% organic cotton.",
            price=25.50,
            stock=500,
            category="Apparel",
            specs={"color": "White", "size": "M"},
        ),
         models.Product(
            name="iPhone 15 Pro",
            description="The latest and greatest iPhone with the A17 Pro chip.",
            price=1099.99,
            stock=80,
            category="Electronics",
            specs={"color": "Natural Titanium", "storage": "512GB"},
        ),
    ]
    db.add_all(products_to_add)
    db.commit()

    # --- Create Orders ---
    iphone_prod = db.query(models.Product).filter(models.Product.name == "iPhone 15 Pro").first()
    macbook_prod = db.query(models.Product).filter(models.Product.name == "MacBook Pro 14-inch").first()

    if iphone_prod and macbook_prod:
        orders_to_add = [
            models.Order(
                product_id=iphone_prod.id,
                quantity=1,
                status="Shipped",
                user_id="user456"
            ),
            models.Order(
                product_id=macbook_prod.id,
                quantity=1,
                status="Delivered",
                user_id="user789"
            ),
            models.Order(
                id=12345, # Specific order ID for testing
                product_id=iphone_prod.id,
                quantity=1,
                status="Pending",
                user_id="user123"
            ),
        ]
        db.add_all(orders_to_add)
        db.commit()

    print("Database has been seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_data()