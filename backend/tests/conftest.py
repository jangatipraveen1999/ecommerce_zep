import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models.models import Category, Product, User
from app.core.security import get_password_hash, create_access_token

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def seed_categories():
    db = TestingSessionLocal()
    cats = [
        Category(name="Fruits & Vegetables", icon="🥦", slug="fruits-vegetables", color="#4CAF50"),
        Category(name="Dairy & Breakfast",   icon="🥛", slug="dairy-breakfast",   color="#2196F3"),
        Category(name="Snacks & Munchies",   icon="🍿", slug="snacks-munchies",   color="#FF9800"),
        Category(name="Beverages",           icon="🧃", slug="beverages",         color="#9C27B0"),
    ]
    for c in cats:
        db.add(c)
    db.commit()
    for c in cats:
        db.refresh(c)
    yield cats
    db.close()


@pytest.fixture
def seed_products(seed_categories):
    db = TestingSessionLocal()
    cats = seed_categories
    products = [
        Product(name="Fresh Tomatoes",      price=25.0, original_price=35.0, unit="500g",  category_id=cats[0].id, discount=28, in_stock=True,  delivery_time=10, rating=4.5, review_count=10, image_url="https://example.com/tomato.jpg"),
        Product(name="Amul Full Cream Milk", price=30.0, original_price=32.0, unit="500ml", category_id=cats[1].id, discount=6,  in_stock=True,  delivery_time=10, rating=4.0, review_count=5,  image_url="https://example.com/milk.jpg"),
        Product(name="Lay's Classic Salted", price=20.0, original_price=25.0, unit="73g",   category_id=cats[2].id, discount=20, in_stock=True,  delivery_time=10, rating=4.2, review_count=8,  image_url="https://example.com/lays.jpg"),
        Product(name="Coca-Cola",            price=40.0, original_price=45.0, unit="750ml", category_id=cats[3].id, discount=11, in_stock=True,  delivery_time=10, rating=4.3, review_count=15, image_url="https://example.com/coke.jpg"),
        Product(name="Baby Spinach",         price=45.0, original_price=55.0, unit="200g",  category_id=cats[0].id, discount=18, in_stock=True,  delivery_time=10, rating=4.1, review_count=3,  image_url="https://example.com/spinach.jpg"),
        Product(name="Out of Stock Item",    price=10.0, original_price=15.0, unit="1pc",   category_id=cats[0].id, discount=0,  in_stock=False, delivery_time=10, rating=3.0, review_count=1,  image_url="https://example.com/oos.jpg"),
    ]
    for p in products:
        db.add(p)
    db.commit()
    for p in products:
        db.refresh(p)
    yield products
    db.close()


@pytest.fixture
def registered_user(client):
    payload = {
        "email": "testuser@zapkart.com",
        "name": "Test User",
        "password": "testpass123",
        "phone": "9999999999",
        "address": "123 Test Street, Bengaluru"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    return {**payload, **response.json()}


@pytest.fixture
def auth_headers(registered_user):
    token = registered_user["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user(client):
    payload = {
        "email": "seconduser@zapkart.com",
        "name": "Second User",
        "password": "secondpass123"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    return {**payload, **response.json()}


@pytest.fixture
def second_auth_headers(second_user):
    token = second_user["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def cart_with_item(client, auth_headers, seed_products):
    product = seed_products[0]
    response = client.post("/api/cart/add", json={"product_id": product.id, "quantity": 1}, headers=auth_headers)
    assert response.status_code == 200
    return client.get("/api/cart/", headers=auth_headers).json()


@pytest.fixture
def placed_order(client, auth_headers, cart_with_item):
    response = client.post("/api/orders/place", json={
        "delivery_address": "123 Test Street, Bengaluru",
        "payment_method": "cod"
    }, headers=auth_headers)
    assert response.status_code == 201
    return response.json()


# ─────────────────────────────────────────
# Aliases for new test files
# ─────────────────────────────────────────
@pytest.fixture
def sample_user(registered_user):
    """Returns dict with user info + access_token."""
    return registered_user


@pytest.fixture
def sample_category(seed_categories):
    """Return first category."""
    return seed_categories[0]


@pytest.fixture
def sample_product(seed_products):
    """Return first product."""
    return seed_products[0]