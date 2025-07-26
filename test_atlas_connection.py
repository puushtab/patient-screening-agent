#!/usr/bin/env python3
"""
Simple MongoDB Atlas Connection Test
Tests basic connectivity to MongoDB Atlas before running the MCP server
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

def test_atlas_connection():
    """Test connection to MongoDB Atlas"""
    
    # Load environment variables
    load_dotenv()
    
    # Get connection details from environment
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    database_name = os.getenv("MONGODB_DATABASE_NAME", "test")
    
    if not connection_string:
        print("❌ MONGODB_CONNECTION_STRING environment variable not set")
        print("\n📋 Setup Instructions:")
        print("1. Copy env.example to .env")
        print("2. Edit .env with your MongoDB Atlas connection string")
        print("3. Run this test again")
        return False
    
    print("🔌 Testing MongoDB Atlas Connection...")
    print(f"📍 Database: {database_name}")
    print(f"🔗 Connection String: {connection_string[:50]}...")
    
    try:
        # Create client with Atlas-optimized settings
        client = MongoClient(
            connection_string,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            maxPoolSize=10,
            retryWrites=True,
            w="majority",
            ssl=True
        )
        
        # Test the connection
        print("⏳ Attempting to connect...")
        client.admin.command('ping')
        
        # Get server info
        server_info = client.server_info()
        print(f"✅ Successfully connected to MongoDB Atlas!")
        print(f"📊 Server Version: {server_info.get('version', 'Unknown')}")
        
        # Test database access
        db = client[database_name]
        collections = db.list_collection_names()
        print(f"📂 Database '{database_name}' accessible")
        print(f"📋 Collections found: {len(collections)}")
        
        if collections:
            print(f"   Collections: {', '.join(collections[:5])}")
            if len(collections) > 5:
                print(f"   ... and {len(collections) - 5} more")
        
        # Test write operation (create a test collection)
        test_collection = db.connection_test
        test_doc = {"test": True, "timestamp": "2024-01-01"}
        result = test_collection.insert_one(test_doc)
        print(f"✅ Write test successful: {result.inserted_id}")
        
        # Clean up test document
        test_collection.delete_one({"_id": result.inserted_id})
        print("🧹 Test document cleaned up")
        
        client.close()
        return True
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your connection string format")
        print("2. Verify username and password")
        print("3. Ensure your IP is whitelisted in Atlas Network Access")
        return False
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the cluster is running")
        print("3. Check Atlas Network Access settings")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 MongoDB Atlas Connection Test")
    print("=" * 50)
    
    success = test_atlas_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Atlas connection test PASSED!")
        print("✅ You can now run the MCP server with: python mongo_mcp_server.py")
    else:
        print("💥 Atlas connection test FAILED!")
        print("❌ Please fix the connection issues before running the MCP server")
        sys.exit(1)

if __name__ == "__main__":
    main() 