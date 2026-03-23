from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.models import User, Category, Product
from app.core.security import get_password_hash


def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    if db.query(Category).first():
        print("Database already seeded.")
        db.close()
        return

    categories_data = [
        {"name": "Fruits & Vegetables", "icon": "🥦", "slug": "fruits-vegetables", "color": "#4CAF50"},
        {"name": "Dairy & Breakfast", "icon": "🥛", "slug": "dairy-breakfast", "color": "#2196F3"},
        {"name": "Snacks & Munchies", "icon": "🍿", "slug": "snacks-munchies", "color": "#FF9800"},
        {"name": "Beverages", "icon": "🧃", "slug": "beverages", "color": "#9C27B0"},
        {"name": "Bakery & Biscuits", "icon": "🍞", "slug": "bakery-biscuits", "color": "#795548"},
        {"name": "Personal Care", "icon": "🧴", "slug": "personal-care", "color": "#E91E63"},
        {"name": "Cleaning Essentials", "icon": "🧹", "slug": "cleaning-essentials", "color": "#00BCD4"},
        {"name": "Instant & Frozen", "icon": "🍜", "slug": "instant-frozen", "color": "#FF5722"},
    ]

    categories = []
    for cat_data in categories_data:
        cat = Category(**cat_data)
        db.add(cat)
        categories.append(cat)
    db.commit()
    for cat in categories:
        db.refresh(cat)

    products_data = [
        # Fruits & Vegetables
        {"name": "Fresh Tomatoes", "price": 25.0, "original_price": 35.0, "unit": "500g", "category_id": categories[0].id, "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=300", "discount": 28, "in_stock": True, "delivery_time": 10},
        {"name": "Baby Spinach", "price": 45.0, "original_price": 55.0, "unit": "200g", "category_id": categories[0].id, "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300", "discount": 18, "in_stock": True, "delivery_time": 10},
        {"name": "Bananas", "price": 40.0, "original_price": 50.0, "unit": "6 pcs", "category_id": categories[0].id, "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300", "discount": 20, "in_stock": True, "delivery_time": 10},
        {"name": "Apples Royal Gala", "price": 120.0, "original_price": 150.0, "unit": "1 kg", "category_id": categories[0].id, "image_url": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=300", "discount": 20, "in_stock": True, "delivery_time": 10},
        # Dairy
        {"name": "Amul Full Cream Milk", "price": 30.0, "original_price": 32.0, "unit": "500ml", "category_id": categories[1].id, "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=300", "discount": 6, "in_stock": True, "delivery_time": 10},
        {"name": "Paneer Fresh", "price": 85.0, "original_price": 100.0, "unit": "200g", "category_id": categories[1].id, "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300", "discount": 15, "in_stock": True, "delivery_time": 10},
        {"name": "Greek Yogurt", "price": 65.0, "original_price": 80.0, "unit": "400g", "category_id": categories[1].id, "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300", "discount": 18, "in_stock": True, "delivery_time": 10},
        # Snacks
        {"name": "Lay's Classic Salted", "price": 20.0, "original_price": 25.0, "unit": "73g", "category_id": categories[2].id, "image_url": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300", "discount": 20, "in_stock": True, "delivery_time": 10},
        {"name": "Bingo Mad Angles", "price": 20.0, "original_price": 22.0, "unit": "90g", "category_id": categories[2].id, "image_url": "https://images.unsplash.com/photo-1613919113640-25732ec5e61f?w=300", "discount": 9, "in_stock": True, "delivery_time": 10},
        # Beverages
        {"name": "Coca-Cola", "price": 40.0, "original_price": 45.0, "unit": "750ml", "category_id": categories[3].id, "image_url": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=300", "discount": 11, "in_stock": True, "delivery_time": 10},
        {"name": "Tropicana Orange Juice", "price": 85.0, "original_price": 99.0, "unit": "1L", "category_id": categories[3].id, "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=300", "discount": 14, "in_stock": True, "delivery_time": 10},
        {"name": "Red Bull Energy Drink", "price": 115.0, "original_price": 125.0, "unit": "250ml", "category_id": categories[3].id, "image_url": "https://images.unsplash.com/photo-1550505095-381b-4b01-a20a-1949f80ecae3?w=300", "discount": 8, "in_stock": True, "delivery_time": 10},
    ]

    for prod_data in products_data:
        db.add(Product(**prod_data))

    # Demo user
    user = User(
        email="demo@zapkart.com",
        name="Demo User",
        phone="+91-9999999999",
        hashed_password=get_password_hash("demo123"),
        address="123, MG Road, Bengaluru, Karnataka - 560001",
    )
    db.add(user)
    db.commit()
    print("✅ Database seeded successfully!")
    db.close()


if __name__ == "__main__":
    seed_database()
