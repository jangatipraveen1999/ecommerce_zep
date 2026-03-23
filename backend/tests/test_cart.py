"""
Tests for Cart endpoints
- GET    /api/cart/
- POST   /api/cart/add
- PUT    /api/cart/{item_id}
- DELETE /api/cart/{item_id}
- DELETE /api/cart/
"""


class TestGetCart:
    def test_get_cart_unauthorized(self, client):
        response = client.get("/api/cart/")
        assert response.status_code == 401

    def test_get_cart_empty_for_new_user(self, client, auth_headers):
        response = client.get("/api/cart/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total_items"] == 0
        assert data["subtotal"] == 0

    def test_get_cart_returns_correct_structure(self, client, auth_headers):
        response = client.get("/api/cart/", headers=auth_headers)
        data = response.json()
        assert "items" in data
        assert "total_items" in data
        assert "subtotal" in data
        assert "delivery_fee" in data
        assert "total" in data


class TestAddToCart:
    def test_add_to_cart_unauthorized(self, client, sample_product):
        response = client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 1
        })
        assert response.status_code == 401

    def test_add_to_cart_success(self, client, auth_headers, sample_product):
        response = client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 1
        }, headers=auth_headers)
        assert response.status_code == 200

    def test_add_to_cart_product_appears_in_cart(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 2
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["product_id"] == sample_product.id
        assert cart["items"][0]["quantity"] == 2

    def test_add_same_product_twice_increases_quantity(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 2
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["quantity"] == 3

    def test_add_nonexistent_product_fails(self, client, auth_headers):
        response = client.post("/api/cart/add", json={
            "product_id": 99999,
            "quantity": 1
        }, headers=auth_headers)
        assert response.status_code == 404

    def test_cart_calculates_subtotal_correctly(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 3
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        expected_subtotal = sample_product.price * 3
        assert cart["subtotal"] == expected_subtotal

    def test_cart_delivery_fee_applied_under_threshold(self, client, auth_headers, sample_product):
        """Delivery fee applied when subtotal < 200."""
        client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 1  # 25.0 < 200
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["delivery_fee"] == 20.0

    def test_cart_free_delivery_above_threshold(self, client, auth_headers, sample_product):
        """Free delivery when subtotal >= 200."""
        client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 10  # 25 * 10 = 250 >= 200
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["delivery_fee"] == 0.0

    def test_cart_total_equals_subtotal_plus_delivery(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 1
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["total"] == cart["subtotal"] + cart["delivery_fee"]

    def test_cart_isolated_between_users(self, client, auth_headers, second_auth_headers, sample_product):
        """Each user has their own cart."""
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 5
        }, headers=auth_headers)

        other_cart = client.get("/api/cart/", headers=second_auth_headers).json()
        assert other_cart["total_items"] == 0


class TestUpdateCart:
    def test_update_cart_item_quantity(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        item_id = cart["items"][0]["id"]

        response = client.put(f"/api/cart/{item_id}", json={"quantity": 5}, headers=auth_headers)
        assert response.status_code == 200

        updated_cart = client.get("/api/cart/", headers=auth_headers).json()
        assert updated_cart["items"][0]["quantity"] == 5

    def test_update_cart_item_to_zero_removes_item(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        item_id = cart["items"][0]["id"]

        client.put(f"/api/cart/{item_id}", json={"quantity": 0}, headers=auth_headers)

        updated_cart = client.get("/api/cart/", headers=auth_headers).json()
        assert updated_cart["items"] == []

    def test_update_nonexistent_item_fails(self, client, auth_headers):
        response = client.put("/api/cart/99999", json={"quantity": 2}, headers=auth_headers)
        assert response.status_code == 404

    def test_update_unauthorized_fails(self, client, sample_product):
        response = client.put("/api/cart/1", json={"quantity": 2})
        assert response.status_code == 401


class TestRemoveFromCart:
    def test_remove_cart_item(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        item_id = cart["items"][0]["id"]

        response = client.delete(f"/api/cart/{item_id}", headers=auth_headers)
        assert response.status_code == 200

        updated_cart = client.get("/api/cart/", headers=auth_headers).json()
        assert updated_cart["items"] == []

    def test_remove_nonexistent_item_fails(self, client, auth_headers):
        response = client.delete("/api/cart/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_remove_unauthorized_fails(self, client):
        response = client.delete("/api/cart/1")
        assert response.status_code == 401


class TestClearCart:
    def test_clear_cart(self, client, auth_headers, sample_product, db):
        from app.models.models import Product, Category
        cat2 = Category(name="Dairy", slug="dairy", icon="🥛", color="#2196F3")
        db.add(cat2)
        db.commit()
        db.refresh(cat2)

        prod2 = Product(
            name="Milk", price=30.0, category_id=cat2.id,
            in_stock=True, delivery_time=10, discount=0, rating=4.0, review_count=0
        )
        db.add(prod2)
        db.commit()
        db.refresh(prod2)

        client.post("/api/cart/add", json={"product_id": sample_product.id, "quantity": 1}, headers=auth_headers)
        client.post("/api/cart/add", json={"product_id": prod2.id, "quantity": 2}, headers=auth_headers)

        response = client.delete("/api/cart/", headers=auth_headers)
        assert response.status_code == 200

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"] == []
        assert cart["total_items"] == 0

    def test_clear_cart_unauthorized_fails(self, client):
        response = client.delete("/api/cart/")
        assert response.status_code == 401
