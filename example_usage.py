#!/usr/bin/env python3
"""
Example usage of MongoDB MCP Server
Demonstrates a practical use case for managing a user database
"""

import asyncio
import json
import os
from datetime import datetime
from mongo_mcp_server import MongoDBMCPServer, MongoDBConfig, CollectionQuery, DocumentInsert, DocumentUpdate, DocumentDelete

async def user_management_example():
    """Example of user management using MongoDB MCP Server"""
    
    # Initialize server
    mongo_server = MongoDBMCPServer()
    
    # Connect to database
    print("🔌 Connecting to MongoDB Atlas...")
    # Get connection string from environment
    connection_string = os.getenv("MONGODB_CONNECTION_STRING", "mongodb+srv://username:password@cluster.mongodb.net/user_management?retryWrites=true&w=majority")
    database_name = os.getenv("MONGODB_DATABASE_NAME", "user_management")
    
    config = MongoDBConfig(
        connection_string=connection_string,
        database_name=database_name,
        timeout_ms=10000,
        use_ssl=True,
        retry_writes=True
    )
    
    result = await mongo_server.connect(config)
    if result.get("status") != "success":
        print(f"❌ Connection failed: {result.get('message')}")
        return
    
    print("✅ Connected successfully!")
    
    # Create sample users
    users = [
        {
            "username": "alice",
            "email": "alice@example.com",
            "full_name": "Alice Johnson",
            "age": 28,
            "role": "admin",
            "created_at": datetime.now().isoformat(),
            "is_active": True
        },
        {
            "username": "bob",
            "email": "bob@example.com",
            "full_name": "Bob Smith",
            "age": 32,
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "is_active": True
        },
        {
            "username": "charlie",
            "email": "charlie@example.com",
            "full_name": "Charlie Brown",
            "age": 25,
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "is_active": False
        }
    ]
    
    # Insert users
    print("\n📝 Inserting users...")
    for user in users:
        insert_params = DocumentInsert(
            collection_name="users",
            document=user
        )
        result = await mongo_server.insert_document(insert_params)
        print(f"Inserted {user['username']}: {result.get('status')}")
    
    # Find all active users
    print("\n🔍 Finding active users...")
    active_query = CollectionQuery(
        collection_name="users",
        query={"is_active": True},
        limit=10,
        sort=[("created_at", -1)]
    )
    
    active_users = await mongo_server.find_documents(active_query)
    print(f"Found {active_users.get('count', 0)} active users")
    
    # Find users by age range
    print("\n🔍 Finding users aged 25-30...")
    age_query = CollectionQuery(
        collection_name="users",
        query={"age": {"$gte": 25, "$lte": 30}},
        limit=10
    )
    
    age_users = await mongo_server.find_documents(age_query)
    print(f"Found {age_users.get('count', 0)} users aged 25-30")
    
    # Update user role
    print("\n✏️ Updating Bob's role to moderator...")
    update_params = DocumentUpdate(
        collection_name="users",
        query={"username": "bob"},
        update={"$set": {"role": "moderator", "updated_at": datetime.now().isoformat()}},
        upsert=False
    )
    
    update_result = await mongo_server.update_documents(update_params)
    print(f"Update result: {update_result.get('message')}")
    
    # Get collection statistics
    print("\n📊 Getting collection statistics...")
    stats = await mongo_server.get_collection_stats("users")
    print(f"Users collection stats: {json.dumps(stats, indent=2)}")
    
    # Find users by role
    print("\n🔍 Finding admin users...")
    admin_query = CollectionQuery(
        collection_name="users",
        query={"role": "admin"},
        limit=10
    )
    
    admin_users = await mongo_server.find_documents(admin_query)
    print(f"Found {admin_users.get('count', 0)} admin users")
    
    # Deactivate inactive users
    print("\n✏️ Deactivating inactive users...")
    deactivate_params = DocumentUpdate(
        collection_name="users",
        query={"is_active": False},
        update={"$set": {"deactivated_at": datetime.now().isoformat()}},
        upsert=False
    )
    
    deactivate_result = await mongo_server.update_documents(deactivate_params)
    print(f"Deactivation result: {deactivate_result.get('message')}")
    
    # Clean up - delete test users (optional)
    print("\n🗑️ Cleaning up test data...")
    cleanup_params = DocumentDelete(
        collection_name="users",
        query={"username": {"$in": ["alice", "bob", "charlie"]}}
    )
    
    cleanup_result = await mongo_server.delete_documents(cleanup_params)
    print(f"Cleanup result: {cleanup_result.get('message')}")
    
    print("\n✅ User management example completed!")

async def ecommerce_example():
    """Example of e-commerce data management"""
    
    print("\n🛒 Starting E-commerce Example")
    print("=" * 40)
    
    mongo_server = MongoDBMCPServer()
    
    # Connect to database
    connection_string = os.getenv("MONGODB_CONNECTION_STRING", "mongodb+srv://username:password@cluster.mongodb.net/ecommerce?retryWrites=true&w=majority")
    database_name = os.getenv("MONGODB_DATABASE_NAME", "ecommerce")
    
    config = MongoDBConfig(
        connection_string=connection_string,
        database_name=database_name,
        timeout_ms=10000,
        use_ssl=True,
        retry_writes=True
    )
    
    result = await mongo_server.connect(config)
    if result.get("status") != "success":
        print(f"❌ Connection failed: {result.get('message')}")
        return
    
    # Create sample products
    products = [
        {
            "product_id": "P001",
            "name": "Laptop",
            "category": "Electronics",
            "price": 999.99,
            "stock": 50,
            "tags": ["computer", "technology", "portable"]
        },
        {
            "product_id": "P002",
            "name": "Smartphone",
            "category": "Electronics",
            "price": 699.99,
            "stock": 100,
            "tags": ["mobile", "technology", "communication"]
        },
        {
            "product_id": "P003",
            "name": "Coffee Maker",
            "category": "Home & Kitchen",
            "price": 89.99,
            "stock": 25,
            "tags": ["kitchen", "appliance", "coffee"]
        }
    ]
    
    # Insert products
    print("📝 Inserting products...")
    for product in products:
        insert_params = DocumentInsert(
            collection_name="products",
            document=product
        )
        result = await mongo_server.insert_document(insert_params)
        print(f"Inserted {product['name']}: {result.get('status')}")
    
    # Find products by category
    print("\n🔍 Finding electronics products...")
    electronics_query = CollectionQuery(
        collection_name="products",
        query={"category": "Electronics"},
        limit=10
    )
    
    electronics = await mongo_server.find_documents(electronics_query)
    print(f"Found {electronics.get('count', 0)} electronics products")
    
    # Find products by price range
    print("\n🔍 Finding products under $100...")
    price_query = CollectionQuery(
        collection_name="products",
        query={"price": {"$lt": 100}},
        limit=10
    )
    
    affordable = await mongo_server.find_documents(price_query)
    print(f"Found {affordable.get('count', 0)} products under $100")
    
    # Update stock levels
    print("\n✏️ Updating stock levels...")
    stock_update = DocumentUpdate(
        collection_name="products",
        query={"product_id": "P001"},
        update={"$inc": {"stock": -5}},
        upsert=False
    )
    
    stock_result = await mongo_server.update_documents(stock_update)
    print(f"Stock update result: {stock_result.get('message')}")
    
    # Get product statistics
    print("\n📊 Getting product statistics...")
    stats = await mongo_server.get_collection_stats("products")
    print(f"Products collection stats: {json.dumps(stats, indent=2)}")
    
    # Clean up
    print("\n🗑️ Cleaning up test data...")
    cleanup_params = DocumentDelete(
        collection_name="products",
        query={"product_id": {"$in": ["P001", "P002", "P003"]}}
    )
    
    cleanup_result = await mongo_server.delete_documents(cleanup_params)
    print(f"Cleanup result: {cleanup_result.get('message')}")
    
    print("✅ E-commerce example completed!")

if __name__ == "__main__":
    print("🚀 MongoDB Atlas MCP Server Examples")
    print("=" * 50)
    print("📋 Prerequisites:")
    print("  1. Set MONGODB_CONNECTION_STRING environment variable with your Atlas connection string")
    print("  2. Set MONGODB_DATABASE_NAME environment variable")
    print("  3. Ensure your IP is whitelisted in Atlas Network Access")
    print("=" * 50)
    
    # Run examples
    asyncio.run(user_management_example())
    asyncio.run(ecommerce_example())
    
    print("\n" + "=" * 50)
    print("🏁 All examples completed!") 