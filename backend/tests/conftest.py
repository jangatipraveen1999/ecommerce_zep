import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models.models import User, Category, Product
from app.core.security import get_password_hash, create_access_token

# ─────────────────────────────────────────
# Test Database Setup
# ─────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test_zapkart.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ─────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_tables():
    """Clean all tables before each test."""
    yield
    db = TestingSessionLocal()
    db.query(User).delete()
    db.query(Product).delete()
    db.query(Category).delete()
    db.commit()
    db.close()


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def db():
    """Database session for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_category(db):
    """Create a sample category."""
    category = Category(
        name="Fruits & Vegetables",
        icon="🥦",
        slug="fruits-vegetables",
        color="#4CAF50"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@pytest.fixture
def sample_product(db, sample_category):
    """Create a sample product."""
    product = Product(
        name="Fresh Tomatoes",
        price=25.0,
        original_price=35.0,
        unit="500g",
        category_id=sample_category.id,
        image_url="https://images.unsplash.com/photo-1546094096?w=300",
        discount=28,
        in_stock=True,
        delivery_time=10,
        rating=4.5,
        review_count=100,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@pytest.fixture
def sample_user(db):
    """Create a sample user."""
    user = User(
        email="test@zapkart.com",
        name="Test User",
        phone="9999999999",
        hashed_password=get_password_hash("testpass123"),
        address="Bengaluru, Karnataka",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(sample_user):
    """Auth headers with JWT token."""
    token = create_access_token({"sub": str(sample_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user(db):
    """Create a second user for isolation tests."""
    user = User(
        email="second@zapkart.com",
        name="Second User",
        hashed_password=get_password_hash("secondpass123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def second_auth_headers(second_user):
    """Auth headers for second user."""
    token = create_access_token({"sub": str(second_user.id)})
    return {"Authorization": f"Bearer {token}"}
