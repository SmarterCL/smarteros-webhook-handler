import hmac
import hashlib
import os

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default-secret-change-me")

def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Verify GitHub webhook signature using HMAC-SHA256
    
    Args:
        payload: Raw request body bytes
        signature: X-Hub-Signature-256 header value
    
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature:
        return False
    
    # Remove 'sha256=' prefix
    if signature.startswith("sha256="):
        signature = signature[7:]
    
    # Calculate expected signature
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Compare using constant-time comparison
    return hmac.compare_digest(expected, signature)
