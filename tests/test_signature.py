import pytest
from src.webhooks.verify import verify_signature
import hmac
import hashlib

def test_verify_valid_signature():
    """Test signature verification with valid signature"""
    payload = b"test payload"
    secret = "test-secret"
    
    # Generate valid signature
    signature = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Mock the environment variable
    import os
    original = os.environ.get("WEBHOOK_SECRET")
    os.environ["WEBHOOK_SECRET"] = secret
    
    from importlib import reload
    from src.webhooks import verify as verify_module
    reload(verify_module)
    
    assert verify_module.verify_signature(payload, signature) is True
    
    # Restore
    if original:
        os.environ["WEBHOOK_SECRET"] = original
    else:
        del os.environ["WEBHOOK_SECRET"]

def test_verify_invalid_signature():
    """Test signature verification with invalid signature"""
    payload = b"test payload"
    signature = "sha256=invalid"
    
    assert verify_signature(payload, signature) is False

def test_verify_empty_signature():
    """Test signature verification with empty signature"""
    payload = b"test payload"
    
    assert verify_signature(payload, "") is False
    assert verify_signature(payload, None) is False

def test_verify_without_prefix():
    """Test signature without sha256= prefix"""
    payload = b"test"
    secret = "test-secret"
    
    # Generate signature without prefix
    sig_no_prefix = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    import os
    os.environ["WEBHOOK_SECRET"] = secret
    from importlib import reload
    from src.webhooks import verify as verify_module
    reload(verify_module)
    
    assert verify_module.verify_signature(payload, sig_no_prefix) is True
