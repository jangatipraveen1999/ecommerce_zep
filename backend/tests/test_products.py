"""
Tests for Products and Categories endpoints
- GET /api/categories/
- GET /api/products/
- GET /api/products/{id}
- GET /api/products/?search=
- GET /api/products/?category_id=
"""
from app.models.models import Category, Product


class TestCategories:
    def test_get_categories_returns_200(self, client):
        response = client.get("/api/categories/")
        assert response.status_code == 200

    def test_get_categories_returns_list(self, client):
        response = client.get("/api/categories/")
        assert isinstance(response.json(), list)

    def test_get_categories_empty_when_no_data(self, client):
        response = client.get("/api/categories/")
        assert response.json() == []

    def test_get_categories_returns_correct_data(self, client, sample_category):
        response = client.get("/api/categories/")
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Fruits & Vegetables"
        assert data[0]["slug"] == "fruits-vegetables"
        assert data[0]["icon"] == "🥦"

    def test_get_categories_multiple(self, client, db):
        cats = [
            Category(name="Dairy", icon="🥛", slug="dairy", color="#2196F3"),
            Category(name="Snacks", icon="🍿", slug="snacks", color="#FF9800"),
            Category(name="Beverages", icon="🧃", slug="beverages", color="#9C27B0"),
        ]
        for cat in cats:
            db.add(cat)
        db.commit()

        response = client.get("/api/categories/")
        assert len(response.json()) == 3

    def test_inactive_categories_not_returned(self, client, db):
        cat = Category(
            name="Hidden Category",
            slug="hidden",
            is_active=False
        )
        db.add(cat)
        db.commit()

        response = client.get("/api/categories/")
        names = [c["name"] for c in response.json()]
        assert "Hidden Category" not in names


class TestProducts:
    def test_get_products_returns_200(self, client):
        response = client.get("/api/products/")
        assert response.status_code == 200

    def test_get_products_returns_list(self, client):
        response = client.get("/api/products/")
        assert isinstance(response.json(), list)

    def test_get_products_empty_when_no_data(self, client):
        response = client.get("/api/products/")
        assert response.json() == []

    def test_get_products_returns_correct_data(self, client, sample_product):
        response = client.get("/api/products/")
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Fresh Tomatoes"
        assert data[0]["price"] == 25.0
        assert data[0]["discount"] == 28

    def test_get_products_includes_category(self, client, sample_product):
        response = client.get("/api/products/")
        product = response.json()[0]
        assert "category" in product
        assert product["category"]["name"] == "Fruits & Vegetables"

    def test_get_single_product_success(self, client, sample_product):
        response = client.get(f"/api/products/{sample_product.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Fresh Tomatoes"

    def test_get_single_product_not_found(self, client):
        response = client.get("/api/products/99999")
        assert response.status_code == 404

    def test_search_products_by_name(self, client, sample_product):
        response = client.get("/api/products/?search=Tomato")
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Fresh Tomatoes"

    def test_search_products_case_insensitive(self, client, sample_product):
        response = client.get("/api/products/?search=tomato")
        assert len(response.json()) == 1

    def test_search_products_no_match(self, client, sample_product):
        response = client.get("/api/products/?search=nonexistentproduct")
        assert response.json() == []

    def test_filter_products_by_category(self, client, sample_product, sample_category):
        response = client.get(f"/api/products/?category_id={sample_category.id}")
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_id"] == sample_category.id

    def test_filter_products_wrong_category(self, client, sample_product):
        response = client.get("/api/products/?category_id=99999")
        assert response.json() == []

    def test_products_pagination_limit(self, client, db, sample_category):
        for i in range(10):
            db.add(Product(
                name=f"Product {i}",
                price=10.0 + i,
                category_id=sample_category.id,
                in_stock=True,
                delivery_time=10,
                discount=0,
                rating=4.0,
                review_count=0,
            ))
        db.commit()

        response = client.get("/api/products/?limit=5")
        assert len(response.json()) == 5

    def test_products_filter_in_stock(self, client, db, sample_category):
        db.add(Product(
            name="Out of Stock Item",
            price=50.0,
            category_id=sample_category.id,
            in_stock=False,
            delivery_time=10,
            discount=0,
            rating=4.0,
            review_count=0,
        ))
        db.commit()

        response = client.get("/api/products/?in_stock=true")
        for product in response.json():
            assert product["in_stock"] is True

    def test_products_filter_min_price(self, client, db, sample_category):
        db.add(Product(
            name="Cheap Item",
            price=5.0,
            category_id=sample_category.id,
            in_stock=True,
            delivery_time=10,
            discount=0,
            rating=4.0,
            review_count=0,
        ))
        db.commit()

        response = client.get("/api/products/?min_price=20")
        for product in response.json():
            assert product["price"] >= 20

    def test_products_filter_max_price(self, client, sample_product):
        response = client.get("/api/products/?max_price=30")
        for product in response.json():
            assert product["price"] <= 30
