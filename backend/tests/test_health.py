"""
Tests for general API endpoints
"""


class TestHealth:
    def test_health_check_returns_200(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self, client):
        response = client.get("/api/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_returns_service_name(self, client):
        response = client.get("/api/health")
        data = response.json()
        assert data["service"] == "ZapKart API"

    def test_root_returns_404(self, client):
        response = client.get("/")
        assert response.status_code == 404

    def test_docs_accessible(self, client):
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_openapi_json_accessible(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200
