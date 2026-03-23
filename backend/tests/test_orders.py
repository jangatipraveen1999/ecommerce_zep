import pytest


class TestPlaceOrder:
    def test_place_order_unauthorized(self, client):
        response = client.post("/api/orders/place", json={"delivery_address": "Test", "payment_method": "cod"})
        assert response.status_code == 401

    def test_place_order_empty_cart_fails(self, client, auth_headers):
        response = client.post("/api/orders/place", json={"delivery_address": "Test", "payment_method": "cod"}, headers=auth_headers)
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_place_order_success(self, client, auth_headers, cart_with_item):
        response = client.post(
            "/api/orders/place",
            json={"delivery_address": "123 Test Street, Bengaluru", "payment_method": "cod"},
            headers=auth_headers
        )
        assert response.status_code == 201

    def test_place_order_returns_order_data(self, client, auth_headers, cart_with_item):
        response = client.post(
            "/api/orders/place",
            json={"delivery_address": "123 Test Street", "payment_method": "cod"},
            headers=auth_headers
        )
        order = response.json()
        assert "id" in order
        assert "status" in order
        assert "total_amount" in order
        assert "items" in order

    def test_place_order_calculates_total_correctly(self, client, auth_headers, seed_products):
        product = seed_products[0]  # price 25.0
        client.post("/api/cart/add", json={"product_id": product.id, "quantity": 1}, headers=auth_headers)
        response = client.post(
            "/api/orders/place",
            json={"delivery_address": "Test", "payment_method": "cod"},
            headers=auth_headers
        )
        order = response.json()
        # 25.0 + 20.0 delivery fee = 45.0
        assert order["total_amount"] == 45.0

    def test_place_order_clears_cart(self, client, auth_headers, cart_with_item):
        client.post("/api/orders/place", json={"delivery_address": "Test", "payment_method": "cod"}, headers=auth_headers)
        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"] == []

    def test_place_order_upi_payment(self, client, auth_headers, cart_with_item):
        response = client.post(
            "/api/orders/place",
            json={"delivery_address": "Test Address", "payment_method": "upi"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["payment_method"] == "upi"

    def test_place_order_missing_address_fails(self, client, auth_headers, cart_with_item):
        response = client.post("/api/orders/place", json={"payment_method": "cod"}, headers=auth_headers)
        assert response.status_code == 422


class TestGetOrders:
    def test_get_orders_unauthorized(self, client):
        response = client.get("/api/orders/")
        assert response.status_code == 401

    def test_get_orders_empty_initially(self, client, auth_headers):
        response = client.get("/api/orders/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_orders_after_placing(self, client, auth_headers, placed_order):
        response = client.get("/api/orders/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_orders_isolated_between_users(self, client, auth_headers, second_auth_headers, placed_order):
        response = client.get("/api/orders/", headers=second_auth_headers)
        assert response.json() == []

    def test_get_single_order_success(self, client, auth_headers, placed_order):
        order_id = placed_order["id"]
        response = client.get(f"/api/orders/{order_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == order_id

    def test_get_nonexistent_order_fails(self, client, auth_headers):
        response = client.get("/api/orders/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_cannot_access_other_users_order(self, client, auth_headers, second_auth_headers, placed_order):
        order_id = placed_order["id"]
        response = client.get(f"/api/orders/{order_id}", headers=second_auth_headers)
        assert response.status_code == 404