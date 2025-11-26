# app/database/connection.py
"""
Database connection module.
- Manages MongoDB connection lifecycle
- Provides database instance for services
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

_client: AsyncIOMotorClient = None
_database = None


async def connect_to_mongo() -> None:
    """Establish connection to MongoDB."""
    global _client, _database
    settings = get_settings()
    
    # MongoDB Atlas requires TLS/SSL
    # For mongodb+srv:// connections, TLS is automatic
    # For mongodb:// connections, we need to enable TLS explicitly
    connection_params = {
        "serverSelectionTimeoutMS": 30000,
        "connectTimeoutMS": 30000
    }
    
    # Check connection string format
    is_srv = settings.mongodb_url.startswith("mongodb+srv://")
    is_atlas = ".mongodb.net" in settings.mongodb_url.lower()
    
    # For Atlas connections, always ensure TLS is enabled
    # SRV connections automatically use TLS
    # Standard connections to Atlas MUST have TLS enabled explicitly
    if is_atlas:
        if is_srv:
            # SRV connections have TLS built-in
            print(f"Using SRV connection string (TLS automatic for Atlas)")
        else:
            # For non-SRV Atlas connections, ALWAYS enable TLS explicitly
            # This ensures TLS works even if connection string format is incomplete
            connection_params["tls"] = True
            connection_params["tlsAllowInvalidCertificates"] = False
            print(f"Enabling TLS for Atlas connection (standard format)")
    
    _client = AsyncIOMotorClient(settings.mongodb_url, **connection_params)
    _database = _client[settings.mongodb_db_name]
    
    try:
        await _client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas")
    except Exception as e:
        # Log warning but allow app to start
        # Connection will be retried when actually used
        # Note: _database is still set so operations can be attempted
        error_type = type(e).__name__
        print(f"Warning: Could not ping MongoDB during startup: {error_type}: {e}")
        print("App will start, connection will be established on first use.")
        print(f"Connection string format: {'SRV' if is_srv else 'Standard'}")
        if "SSL" in str(e) or "TLS" in str(e) or "handshake" in str(e).lower():
            print("TLS/SSL issue detected. Please verify:")
            print("  1. Your connection string is correct (use mongodb+srv:// for Atlas)")
            print("  2. Your IP address is whitelisted in MongoDB Atlas")
            print("  3. Your network/firewall allows outbound connections to MongoDB")


async def close_mongo_connection() -> None:
    """Close MongoDB connection."""
    global _client
    if _client:
        _client.close()


def get_database():
    """Get database instance."""
    if _database is None:
        print("ERROR: Database is None when get_database() is called")
        print(f"Client is None: {_client is None}")
        raise RuntimeError("Database not initialized")
    print(f"Database retrieved: {_database.name}")
    return _database
