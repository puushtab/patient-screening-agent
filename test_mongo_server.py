#!/usr/bin/env python3
"""
Test script for MongoDB MCP Server
Demonstrates usage of all available tools
"""

import asyncio
import json
import os
from mongo_mcp_server import MongoDBMCPServer, MongoDBConfig, CollectionQuery, DocumentInsert, DocumentUpdate, DocumentDelete

async def test_mongodb_mcp_server():
    """Test all MongoDB MCP server functionality"""
    
    # Initialize server
    mongo_server = MongoDBMCPServer()
    
    # Test connection
    print("🔌 Testing MongoDB Atlas connection...")
    # Get connection string from environment or use default
    connection_string = os.getenv("MONGODB_CONNECTION_STRING", "mongodb+srv://username:password@cluster.mongodb.net/test_database?retryWrites=true&w=majority")
    database_name = os.getenv("MONGODB_DATABASE_NAME", "test_database")
    
    config = MongoDBConfig(
        connection_string=connection_string,
        database_name=database_name,
        timeout_ms=10000,
        use_ssl=True,
        retry_writes=True
    )
    
    result = await mongo_server.connect(config)
    print(f"Connection result: {json.dumps(result, indent=2)}")
    
    if result.get("status") != "success":
        print("❌ Failed to connect to MongoDB Atlas. Please check your connection string and network access.")
        print("Make sure to:")
        print("  1. Set MONGODB_CONNECTION_STRING environment variable")
        print("  2. Add your IP to Atlas Network Access whitelist")
        print("  3. Verify database user credentials")
        return
    
    print("✅ Connected to MongoDB Atlas successfully!")
    
    # Test listing collections
    print("\n📋 Testing list collections...")
    collections = await mongo_server.list_collections()
    print(f"Collections: {collections}")
    
    # Test inserting documents
    print("\n📝 Testing document insertion...")
    insert_params = DocumentInsert(
        collection_name="test_users",
        document={
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "city": "New York"
        }
    )
    
    insert_result = await mongo_server.insert_document(insert_params)
    print(f"Insert result: {json.dumps(insert_result, indent=2)}")
    
    # Insert another document
    insert_params2 = DocumentInsert(
        collection_name="test_users",
        document={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 25,
            "city": "Los Angeles"
        }
    )
    
    insert_result2 = await mongo_server.insert_document(insert_params2)
    print(f"Second insert result: {json.dumps(insert_result2, indent=2)}")
    
    # Test finding documents
    print("\n🔍 Testing document search...")
    query_params = CollectionQuery(
        collection_name="test_users",
        query={},
        limit=10,
        sort=[("name", 1)]
    )
    
    find_result = await mongo_server.find_documents(query_params)
    print(f"Find result: {json.dumps(find_result, indent=2)}")
    
    # Test finding documents with filter
    print("\n🔍 Testing filtered search...")
    filter_query_params = CollectionQuery(
        collection_name="test_users",
        query={"age": {"$gte": 25}},
        limit=5
    )
    
    filter_result = await mongo_server.find_documents(filter_query_params)
    print(f"Filtered find result: {json.dumps(filter_result, indent=2)}")
    
    # Test updating documents
    print("\n✏️ Testing document update...")
    update_params = DocumentUpdate(
        collection_name="test_users",
        query={"email": "john@example.com"},
        update={"$set": {"age": 31, "updated": True}},
        upsert=False
    )
    
    update_result = await mongo_server.update_documents(update_params)
    print(f"Update result: {json.dumps(update_result, indent=2)}")
    
    # Test collection stats
    print("\n📊 Testing collection statistics...")
    stats_result = await mongo_server.get_collection_stats("test_users")
    print(f"Collection stats: {json.dumps(stats_result, indent=2)}")
    
    # Test deleting documents
    print("\n🗑️ Testing document deletion...")
    delete_params = DocumentDelete(
        collection_name="test_users",
        query={"email": "jane@example.com"}
    )
    
    delete_result = await mongo_server.delete_documents(delete_params)
    print(f"Delete result: {json.dumps(delete_result, indent=2)}")
    
    # Verify deletion by finding remaining documents
    print("\n🔍 Verifying deletion...")
    verify_query = CollectionQuery(
        collection_name="test_users",
        query={},
        limit=10
    )
    
    verify_result = await mongo_server.find_documents(verify_query)
    print(f"Remaining documents: {json.dumps(verify_result, indent=2)}")
    
    print("\n✅ All tests completed!")

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🧪 Testing error handling...")
    
    mongo_server = MongoDBMCPServer()
    
    # Test operations without connection
    print("Testing operations without connection...")
    
    # Try to list collections without connection
    collections = await mongo_server.list_collections()
    print(f"Collections without connection: {collections}")
    
    # Try to find documents without connection
    query_params = CollectionQuery(
        collection_name="test_users",
        query={},
        limit=10
    )
    
    find_result = await mongo_server.find_documents(query_params)
    print(f"Find without connection: {json.dumps(find_result, indent=2)}")
    
    # Test invalid connection
    print("\nTesting invalid connection...")
    invalid_config = MongoDBConfig(
        connection_string="mongodb+srv://invalid:invalid@invalid-cluster.mongodb.net/test?retryWrites=true&w=majority",
        database_name="test_database",
        timeout_ms=5000,
        use_ssl=True,
        retry_writes=True
    )
    
    invalid_result = await mongo_server.connect(invalid_config)
    print(f"Invalid connection result: {json.dumps(invalid_result, indent=2)}")

if __name__ == "__main__":
    print("🚀 Starting MongoDB Atlas MCP Server Tests")
    print("=" * 50)
    print("📋 Prerequisites:")
    print("  1. Set MONGODB_CONNECTION_STRING environment variable")
    print("  2. Set MONGODB_DATABASE_NAME environment variable")
    print("  3. Ensure your IP is whitelisted in Atlas Network Access")
    print("=" * 50)
    
    # Run main tests
    asyncio.run(test_mongodb_mcp_server())
    
    # Run error handling tests
    asyncio.run(test_error_handling())
    
    print("\n" + "=" * 50)
    print("🏁 All tests finished!") 