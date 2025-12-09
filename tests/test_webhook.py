import pytest
from fastapi.testclient import TestClient
from src.main import app
import hmac
import hashlib
import os

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "SmarterOS Webhook Handler"
    assert "version" in data

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_webhook_without_signature():
    """Test webhook accepts request without signature"""
    payload = {"action": "test", "data": "hello"}
    response = client.post(
        "/webhooks/test",
        json=payload,
        headers={"X-GitHub-Delivery": "test-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    assert data["delivery_id"] == "test-123"

def test_webhook_with_valid_signature():
    """Test webhook with valid HMAC signature"""
    payload = b'{"action": "test", "data": "hello"}'
    secret = os.getenv("WEBHOOK_SECRET", "default-secret-change-me")
    
    signature = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    response = client.post(
        "/webhooks/test",
        content=payload,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": signature,
            "X-GitHub-Delivery": "test-456"
        }
    )
    assert response.status_code == 200

def test_webhook_with_invalid_signature():
    """Test webhook rejects invalid signature"""
    payload = {"action": "test", "data": "hello"}
    response = client.post(
        "/webhooks/test",
        json=payload,
        headers={
            "X-Hub-Signature-256": "sha256=invalid",
            "X-GitHub-Delivery": "test-789"
        }
    )
    assert response.status_code == 401

def test_webhook_with_invalid_json():
    """Test webhook rejects invalid JSON"""
    response = client.post(
        "/webhooks/test",
        content=b"not json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
