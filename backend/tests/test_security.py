"""
Unit tests for security utilities
- get_password_hash
- verify_password
- create_access_token
- decode_token
"""
import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_token,
)
from datetime import timedelta


class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        hashed = get_password_hash("mypassword123")
        assert isinstance(hashed, str)

    def test_hash_is_different_from_plain(self):
        plain = "mypassword123"
        hashed = get_password_hash(plain)
        assert hashed != plain

    def test_same_password_different_hash(self):
        """bcrypt generates different salt each time."""
        hash1 = get_password_hash("samepassword")
        hash2 = get_password_hash("samepassword")
        assert hash1 != hash2

    def test_verify_correct_password(self):
        plain = "correctpassword"
        hashed = get_password_hash(plain)
        assert verify_password(plain, hashed) is True

    def test_verify_wrong_password(self):
        hashed = get_password_hash("correctpassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_empty_password(self):
        hashed = get_password_hash("somepassword")
        assert verify_password("", hashed) is False

    def test_hash_length_is_reasonable(self):
        hashed = get_password_hash("testpassword")
        assert len(hashed) > 20


class TestJWTToken:
    def test_create_token_returns_string(self):
        token = create_access_token({"sub": "1"})
        assert isinstance(token, str)

    def test_create_token_has_three_parts(self):
        """JWT format: header.payload.signature"""
        token = create_access_token({"sub": "1"})
        parts = token.split(".")
        assert len(parts) == 3

    def test_decode_valid_token(self):
        token = create_access_token({"sub": "42"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"

    def test_decode_invalid_token_returns_none(self):
        result = decode_token("invalid.token.here")
        assert result is None

    def test_decode_empty_token_returns_none(self):
        result = decode_token("")
        assert result is None

    def test_decode_malformed_token_returns_none(self):
        result = decode_token("notavalidtoken")
        assert result is None

    def test_token_contains_expiry(self):
        token = create_access_token({"sub": "1"})
        payload = decode_token(token)
        assert "exp" in payload

    def test_token_with_custom_expiry(self):
        token = create_access_token(
            {"sub": "1"},
            expires_delta=timedelta(hours=1)
        )
        payload = decode_token(token)
        assert payload is not None

    def test_expired_token_returns_none(self):
        token = create_access_token(
            {"sub": "1"},
            expires_delta=timedelta(seconds=-1)  # already expired
        )
        result = decode_token(token)
        assert result is None

    def test_token_preserves_custom_data(self):
        data = {"sub": "99", "role": "admin", "name": "Praveen"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["sub"] == "99"
        assert payload["role"] == "admin"
        assert payload["name"] == "Praveen"
