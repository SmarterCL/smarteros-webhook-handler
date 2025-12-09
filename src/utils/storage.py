import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any

DB_PATH = os.getenv("DB_PATH", "webhooks.db")

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhook_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_delivery_id 
        ON webhook_events(delivery_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON webhook_events(timestamp)
    """)
    
    conn.commit()
    conn.close()

def save_webhook_event(event_data: Dict[str, Any]) -> int:
    """
    Save webhook event to database
    
    Args:
        event_data: Event data dictionary
        
    Returns:
        Event ID
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO webhook_events (delivery_id, event_type, timestamp, payload)
        VALUES (?, ?, ?, ?)
    """, (
        event_data["delivery_id"],
        event_data["event_type"],
        event_data["timestamp"],
        json.dumps(event_data["payload"])
    ))
    
    event_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return event_id

def get_recent_events(limit: int = 10):
    """Get recent webhook events"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM webhook_events 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return events
