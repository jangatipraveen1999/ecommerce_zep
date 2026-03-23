import pytest


class TestGetCart:
    def test_get_cart_unauthorized(self, client):
        response = client.get("/api/cart/")
        assert response.status_code == 401

    def test_get_cart_empty_for_new_user(self, client, auth_headers):
        response = client.get("/api/cart/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["items"] == []

    def test_get_cart_returns_correct_structure(self, client, auth_headers):
        response = client.get("/api/cart/", headers=auth_headers)
        data = response.json()
        assert "items" in data
        assert "total_items" in data
        assert "subtotal" in data
        assert "delivery_fee" in data
        assert "total" in data


class TestAddToCart:
    def test_add_to_cart_unauthorized(self, client, seed_products):
        response = client.post("/api/cart/add", json={"product_id": seed_products[0].id, "quantity": 1})
        assert response.status_code == 401

    def test_add_to_cart_success(self, client, auth_headers, seed_products):
        response = client.post(
            "/api/cart/add",
            json={"product_id": seed_products[0].id, "quantity": 1},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_add_to_cart_product_appears_in_cart(self, client, auth_headers, seed_products):
        client.post("/api/cart/add", json={"product_id": seed_products[0].id, "quantity": 1}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["product_id"] == seed_products[0].id

    def test_add_same_product_twice_increases_quantity(self, client, auth_headers, seed_products):
        client.post("/api/cart/add", json={"product_id": seed_products[0].id, "quantity": 1}, headers=auth_headers)
        client.post("/api/cart/add", json={"product_id": seed_products[0].id, "quantity": 1}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["quantity"] == 2

    def test_add_nonexistent_product_fails(self, client, auth_headers):
        response = client.post("/api/cart/add", json={"product_id": 99999, "quantity": 1}, headers=auth_headers)
        assert response.status_code == 404

    def test_cart_calculates_subtotal_correctly(self, client, auth_headers, seed_products):
        product = seed_products[0]  # price = 25.0
        client.post("/api/cart/add", json={"product_id": product.id, "quantity": 3}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["subtotal"] == product.price * 3

    def test_cart_delivery_fee_applied_under_threshold(self, client, auth_headers, seed_products):
        product = seed_products[0]  # price 25.0 — below 200 threshold
        client.post("/api/cart/add", json={"product_id": product.id, "quantity": 1}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["delivery_fee"] == 20.0

    def test_cart_free_delivery_above_threshold(self, client, auth_headers, seed_products):
        # Add enough items to exceed ₹200 threshold
        product = seed_products[3]  # Coca-Cola 40.0
        client.post("/api/cart/add", json={"product_id": product.id, "quantity": 6}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["subtotal"] >= 200
        assert cart["delivery_fee"] == 0.0

    def test_cart_total_equals_subtotal_plus_delivery(self, client, auth_headers, seed_products):
        client.post("/api/cart/add", json={"product_id": seed_products[0].id, "quantity": 1}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["total"] == cart["subtotal"] + cart["delivery_fee"]

    def test_cart_isolated_between_users(self, client, auth_headers, second_auth_headers, seed_products):
        client.post("/api/cart/add", json={"product_id": seed_products[0].id, "quantity": 1}, headers=auth_headers)
        cart2 = client.get("/api/cart/", headers=second_auth_headers).json()
        assert cart2["items"] == []


class TestUpdateCart:
    def test_update_cart_item_quantity(self, client, auth_headers, cart_with_item):
        item_id = cart_with_item["items"][0]["id"]
        response = client.put(f"/api/cart/{item_id}", json={"quantity": 5}, headers=auth_headers)
        assert response.status_code == 200
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"][0]["quantity"] == 5

    def test_update_cart_item_to_zero_removes_item(self, client, auth_headers, cart_with_item):
        item_id = cart_with_item["items"][0]["id"]
        client.put(f"/api/cart/{item_id}", json={"quantity": 0}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"] == []

    def test_update_nonexistent_item_fails(self, client, auth_headers):
        response = client.put("/api/cart/99999", json={"quantity": 2}, headers=auth_headers)
        assert response.status_code == 404

    def test_update_unauthorized_fails(self, client):
        response = client.put("/api/cart/1", json={"quantity": 2})
        assert response.status_code == 401


class TestRemoveFromCart:
    def test_remove_cart_item(self, client, auth_headers, cart_with_item):
        item_id = cart_with_item["items"][0]["id"]
        response = client.delete(f"/api/cart/{item_id}", headers=auth_headers)
        assert response.status_code == 200
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"] == []

    def test_remove_nonexistent_item_fails(self, client, auth_headers):
        response = client.delete("/api/cart/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_remove_unauthorized_fails(self, client):
        response = client.delete("/api/cart/1")
        assert response.status_code == 401


class TestClearCart:
    def test_clear_cart(self, client, auth_headers, cart_with_item):
        response = client.delete("/api/cart/", headers=auth_headers)
        assert response.status_code == 200
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"] == []

    def test_clear_cart_unauthorized_fails(self, client):
        response = client.delete("/api/cart/")
        assert response.status_code == 401