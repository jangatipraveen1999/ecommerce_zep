import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db

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
client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_categories():
    response = client.get("/api/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_register_user():
    response = client.post("/api/auth/register", json={
        "email": "test@zapkart.com",
        "name": "Test User",
        "password": "testpass123"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_login_success():
    response = client.post("/api/auth/login", json={
        "email": "test@zapkart.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_cart_unauthorized():
    response = client.get("/api/cart/")
    assert response.status_code == 401