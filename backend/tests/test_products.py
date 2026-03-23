import pytest


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

    def test_get_categories_returns_correct_data(self, client, seed_categories):
        response = client.get("/api/categories/")
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Fruits & Vegetables"
        assert data[0]["slug"] == "fruits-vegetables"

    def test_get_categories_multiple(self, client, seed_categories):
        response = client.get("/api/categories/")
        assert len(response.json()) == 4

    def test_inactive_categories_not_returned(self, client, seed_categories):
        # All seeded categories are active by default
        response = client.get("/api/categories/")
        assert response.status_code == 200


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

    def test_get_products_returns_correct_data(self, client, seed_products):
        response = client.get("/api/products/")
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Fresh Tomatoes"
        assert data[0]["price"] == 25.0

    def test_get_products_includes_category(self, client, seed_products):
        response = client.get("/api/products/")
        product = response.json()[0]
        assert "category" in product
        assert product["category"]["name"] == "Fruits & Vegetables"

    def test_get_single_product_success(self, client, seed_products):
        product_id = seed_products[0].id
        response = client.get(f"/api/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Fresh Tomatoes"

    def test_get_single_product_not_found(self, client):
        response = client.get("/api/products/99999")
        assert response.status_code == 404

    def test_search_products_by_name(self, client, seed_products):
        response = client.get("/api/products/?search=Tomatoes")
        data = response.json()
        assert len(data) >= 1
        assert "Tomatoes" in data[0]["name"]

    def test_search_products_case_insensitive(self, client, seed_products):
        response = client.get("/api/products/?search=tomatoes")
        assert len(response.json()) >= 1

    def test_search_products_no_match(self, client, seed_products):
        response = client.get("/api/products/?search=xyznonexistent")
        assert response.json() == []

    def test_filter_products_by_category(self, client, seed_products):
        cat_id = seed_products[0].category_id
        response = client.get(f"/api/products/?category_id={cat_id}")
        data = response.json()
        assert len(data) >= 1
        assert all(p["category_id"] == cat_id for p in data)

    def test_filter_products_wrong_category(self, client, seed_products):
        response = client.get("/api/products/?category_id=99999")
        assert response.json() == []

    def test_products_pagination_limit(self, client, seed_products):
        response = client.get("/api/products/?limit=3")
        assert len(response.json()) <= 3

    def test_products_filter_in_stock(self, client, seed_products):
        response = client.get("/api/products/?in_stock=true")
        data = response.json()
        assert all(p["in_stock"] for p in data)

    def test_products_filter_min_price(self, client, seed_products):
        response = client.get("/api/products/?min_price=30")
        data = response.json()
        assert all(p["price"] >= 30 for p in data)

    def test_products_filter_max_price(self, client, seed_products):
        response = client.get("/api/products/?max_price=30")
        data = response.json()
        assert all(p["price"] <= 30 for p in data)