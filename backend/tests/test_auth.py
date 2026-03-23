"""
Tests for Authentication endpoints
- POST /api/auth/register
- POST /api/auth/login
- GET  /api/auth/me
"""
import pytest


class TestRegister:
    def test_register_success(self, client):
        response = client.post("/api/auth/register", json={
            "email": "new@zapkart.com",
            "name": "New User",
            "password": "newpass123",
            "phone": "9876543210",
            "address": "Bengaluru"
        })
        assert response.status_code == 201

    def test_register_returns_access_token(self, client):
        response = client.post("/api/auth/register", json={
            "email": "token@zapkart.com",
            "name": "Token User",
            "password": "tokenpass123"
        })
        data = response.json()
        assert "access_token" in data
        assert len(data["access_token"]) > 0

    def test_register_returns_token_type_bearer(self, client):
        response = client.post("/api/auth/register", json={
            "email": "bearer@zapkart.com",
            "name": "Bearer User",
            "password": "bearerpass123"
        })
        assert response.json()["token_type"] == "bearer"

    def test_register_returns_user_data(self, client):
        response = client.post("/api/auth/register", json={
            "email": "userdata@zapkart.com",
            "name": "Data User",
            "password": "datapass123"
        })
        user = response.json()["user"]
        assert user["email"] == "userdata@zapkart.com"
        assert user["name"] == "Data User"
        assert "id" in user
        assert "hashed_password" not in user  # password not exposed

    def test_register_duplicate_email_fails(self, client, sample_user):
        response = client.post("/api/auth/register", json={
            "email": "test@zapkart.com",  # same as sample_user
            "name": "Duplicate User",
            "password": "duppass123"
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email_fails(self, client):
        response = client.post("/api/auth/register", json={
            "email": "not-an-email",
            "name": "Bad Email User",
            "password": "badpass123"
        })
        assert response.status_code == 422

    def test_register_missing_name_fails(self, client):
        response = client.post("/api/auth/register", json={
            "email": "noname@zapkart.com",
            "password": "noname123"
        })
        assert response.status_code == 422

    def test_register_missing_password_fails(self, client):
        response = client.post("/api/auth/register", json={
            "email": "nopw@zapkart.com",
            "name": "No Password User"
        })
        assert response.status_code == 422

    def test_register_without_optional_fields(self, client):
        """Phone and address are optional."""
        response = client.post("/api/auth/register", json={
            "email": "minimal@zapkart.com",
            "name": "Minimal User",
            "password": "minimalpass123"
        })
        assert response.status_code == 201

    def test_register_empty_body_fails(self, client):
        response = client.post("/api/auth/register", json={})
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, sample_user):
        response = client.post("/api/auth/login", json={
            "email": "test@zapkart.com",
            "password": "testpass123"
        })
        assert response.status_code == 200

    def test_login_returns_access_token(self, client, sample_user):
        response = client.post("/api/auth/login", json={
            "email": "test@zapkart.com",
            "password": "testpass123"
        })
        assert "access_token" in response.json()

    def test_login_wrong_password_fails(self, client, sample_user):
        response = client.post("/api/auth/login", json={
            "email": "test@zapkart.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_wrong_email_fails(self, client):
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@zapkart.com",
            "password": "somepass123"
        })
        assert response.status_code == 401

    def test_login_invalid_email_format_fails(self, client):
        response = client.post("/api/auth/login", json={
            "email": "not-an-email",
            "password": "somepass123"
        })
        assert response.status_code == 422

    def test_login_empty_body_fails(self, client):
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 422

    def test_login_returns_user_info(self, client, sample_user):
        response = client.post("/api/auth/login", json={
            "email": "test@zapkart.com",
            "password": "testpass123"
        })
        user = response.json()["user"]
        assert user["email"] == "test@zapkart.com"
        assert user["name"] == "Test User"


class TestGetMe:
    def test_get_me_success(self, client, auth_headers, sample_user):
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200

    def test_get_me_returns_correct_user(self, client, auth_headers, sample_user):
        response = client.get("/api/auth/me", headers=auth_headers)
        data = response.json()
        assert data["email"] == sample_user["user"]["email"]
        assert data["name"] == sample_user["user"]["name"]
        assert data["id"] == sample_user["user"]["id"]

    def test_get_me_without_token_fails(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_me_with_invalid_token_fails(self, client):
        response = client.get("/api/auth/me", headers={
            "Authorization": "Bearer invalid.token.here"
        })
        assert response.status_code == 401

    def test_get_me_with_malformed_header_fails(self, client):
        response = client.get("/api/auth/me", headers={
            "Authorization": "NotBearer sometoken"
        })
        assert response.status_code == 401
