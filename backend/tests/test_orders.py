"""
Tests for Orders endpoints
- POST /api/orders/place
- GET  /api/orders/
- GET  /api/orders/{id}
"""


class TestPlaceOrder:
    def test_place_order_unauthorized(self, client):
        response = client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        })
        assert response.status_code == 401

    def test_place_order_empty_cart_fails(self, client, auth_headers):
        response = client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers)
        assert response.status_code == 400

    def test_place_order_success(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id,
            "quantity": 2
        }, headers=auth_headers)

        response = client.post("/api/orders/place", json={
            "delivery_address": "123 MG Road, Bengaluru",
            "payment_method": "cod"
        }, headers=auth_headers)
        assert response.status_code == 201

    def test_place_order_returns_order_data(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 2
        }, headers=auth_headers)

        response = client.post("/api/orders/place", json={
            "delivery_address": "123 MG Road",
            "payment_method": "cod"
        }, headers=auth_headers)

        order = response.json()
        assert "id" in order
        assert order["status"] == "placed"
        assert order["delivery_address"] == "123 MG Road"
        assert order["payment_method"] == "cod"
        assert len(order["items"]) == 1

    def test_place_order_calculates_total_correctly(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 3
        }, headers=auth_headers)

        response = client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers)

        order = response.json()
        # 25.0 * 3 = 75, + 20 delivery fee = 95
        assert order["total_amount"] == 95.0

    def test_place_order_clears_cart(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)

        client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers)

        cart = client.get("/api/cart/", headers=auth_headers).json()
        assert cart["items"] == []

    def test_place_order_upi_payment(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)

        response = client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "upi"
        }, headers=auth_headers)

        assert response.json()["payment_method"] == "upi"

    def test_place_order_missing_address_fails(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)

        response = client.post("/api/orders/place", json={
            "payment_method": "cod"
        }, headers=auth_headers)
        assert response.status_code == 422


class TestGetOrders:
    def test_get_orders_unauthorized(self, client):
        response = client.get("/api/orders/")
        assert response.status_code == 401

    def test_get_orders_empty_initially(self, client, auth_headers):
        response = client.get("/api/orders/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_orders_after_placing(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)
        client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers)

        response = client.get("/api/orders/", headers=auth_headers)
        assert len(response.json()) == 1

    def test_get_orders_isolated_between_users(self, client, auth_headers, second_auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)
        client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers)

        other_orders = client.get("/api/orders/", headers=second_auth_headers).json()
        assert other_orders == []

    def test_get_single_order_success(self, client, auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)
        order = client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers).json()

        response = client.get(f"/api/orders/{order['id']}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == order["id"]

    def test_get_nonexistent_order_fails(self, client, auth_headers):
        response = client.get("/api/orders/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_cannot_access_other_users_order(self, client, auth_headers, second_auth_headers, sample_product):
        client.post("/api/cart/add", json={
            "product_id": sample_product.id, "quantity": 1
        }, headers=auth_headers)
        order = client.post("/api/orders/place", json={
            "delivery_address": "Test Address",
            "payment_method": "cod"
        }, headers=auth_headers).json()

        response = client.get(f"/api/orders/{order['id']}", headers=second_auth_headers)
        assert response.status_code == 404
