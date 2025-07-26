#!/usr/bin/env python3
"""
MongoDB MCP Server using FastMCP
Provides tools to interact with MongoDB collections
"""

import os
import asyncio
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoDBConfig(BaseModel):
    """MongoDB Atlas connection configuration"""
    connection_string: str = Field(..., description="MongoDB Atlas connection string (mongodb+srv://...)")
    database_name: str = Field(..., description="Database name")
    timeout_ms: int = Field(default=10000, description="Connection timeout in milliseconds (Atlas may need longer)")
    use_ssl: bool = Field(default=True, description="Use SSL connection (recommended for Atlas)")
    retry_writes: bool = Field(default=True, description="Enable retry writes for Atlas")

class CollectionQuery(BaseModel):
    """Query parameters for collection operations"""
    collection_name: str = Field(..., description="Name of the collection")
    query: Optional[Dict[str, Any]] = Field(default={}, description="MongoDB query filter")
    limit: Optional[int] = Field(default=100, description="Maximum number of documents to return")
    sort: Optional[List[tuple]] = Field(default=None, description="Sort criteria")

class DocumentInsert(BaseModel):
    """Document insertion parameters"""
    collection_name: str = Field(..., description="Name of the collection")
    document: Dict[str, Any] = Field(..., description="Document to insert")

class DocumentUpdate(BaseModel):
    """Document update parameters"""
    collection_name: str = Field(..., description="Name of the collection")
    query: Dict[str, Any] = Field(..., description="Query to find documents to update")
    update: Dict[str, Any] = Field(..., description="Update operations")
    upsert: bool = Field(default=False, description="Create document if it doesn't exist")

class DocumentDelete(BaseModel):
    """Document deletion parameters"""
    collection_name: str = Field(..., description="Name of the collection")
    query: Dict[str, Any] = Field(..., description="Query to find documents to delete")

class MongoDBMCPServer:
    """MongoDB MCP Server implementation"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.config = None
        
    async def connect(self, config: MongoDBConfig) -> Dict[str, Any]:
        """Connect to MongoDB Atlas database"""
        try:
            self.config = config
            
            # Atlas-specific connection options
            connection_options = {
                "serverSelectionTimeoutMS": config.timeout_ms,
                "connectTimeoutMS": config.timeout_ms,
                "socketTimeoutMS": config.timeout_ms,
                "maxPoolSize": 10,
                "retryWrites": config.retry_writes,
                "w": "majority"
            }
            
            # Add SSL settings for Atlas
            if config.use_ssl:
                connection_options.update({
                    "ssl": True,
                    "ssl_cert_reqs": "CERT_NONE"  # Atlas handles certificate validation
                })
            
            self.client = MongoClient(
                config.connection_string,
                **connection_options
            )
            
            # Test the connection with a more comprehensive ping
            self.client.admin.command('ping')
            server_info = self.client.server_info()
            
            self.db = self.client[config.database_name]
            
            return {
                "status": "success",
                "message": f"Successfully connected to MongoDB Atlas database: {config.database_name}",
                "server_version": server_info.get("version", "Unknown"),
                "atlas_connection": True,
                "collections": await self.list_collections()
            }
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            return {
                "status": "error",
                "message": f"Failed to connect to MongoDB Atlas: {str(e)}. Check your connection string and network access."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error connecting to Atlas: {str(e)}"
            }
    
    async def list_collections(self) -> List[str]:
        """List all collections in the database"""
        if not self.db:
            return []
        return self.db.list_collection_names()
    
    async def find_documents(self, params: CollectionQuery) -> Dict[str, Any]:
        """Find documents in a collection"""
        if not self.db:
            return {"status": "error", "message": "Not connected to database"}
        
        try:
            collection = self.db[params.collection_name]
            
            # Build the query
            cursor = collection.find(params.query)
            
            # Apply sorting if specified
            if params.sort:
                cursor = cursor.sort(params.sort)
            
            # Apply limit
            cursor = cursor.limit(params.limit)
            
            # Convert cursor to list
            documents = list(cursor)
            
            return {
                "status": "success",
                "count": len(documents),
                "documents": documents
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error finding documents: {str(e)}"
            }
    
    async def insert_document(self, params: DocumentInsert) -> Dict[str, Any]:
        """Insert a document into a collection"""
        if not self.db:
            return {"status": "error", "message": "Not connected to database"}
        
        try:
            collection = self.db[params.collection_name]
            result = collection.insert_one(params.document)
            
            return {
                "status": "success",
                "inserted_id": str(result.inserted_id),
                "message": f"Document inserted successfully into {params.collection_name}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error inserting document: {str(e)}"
            }
    
    async def update_documents(self, params: DocumentUpdate) -> Dict[str, Any]:
        """Update documents in a collection"""
        if not self.db:
            return {"status": "error", "message": "Not connected to database"}
        
        try:
            collection = self.db[params.collection_name]
            result = collection.update_many(
                params.query,
                params.update,
                upsert=params.upsert
            )
            
            return {
                "status": "success",
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None,
                "message": f"Updated {result.modified_count} documents in {params.collection_name}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error updating documents: {str(e)}"
            }
    
    async def delete_documents(self, params: DocumentDelete) -> Dict[str, Any]:
        """Delete documents from a collection"""
        if not self.db:
            return {"status": "error", "message": "Not connected to database"}
        
        try:
            collection = self.db[params.collection_name]
            result = collection.delete_many(params.query)
            
            return {
                "status": "success",
                "deleted_count": result.deleted_count,
                "message": f"Deleted {result.deleted_count} documents from {params.collection_name}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error deleting documents: {str(e)}"
            }
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection"""
        if not self.db:
            return {"status": "error", "message": "Not connected to database"}
        
        try:
            collection = self.db[collection_name]
            stats = self.db.command("collstats", collection_name)
            
            return {
                "status": "success",
                "collection_name": collection_name,
                "count": stats.get("count", 0),
                "size": stats.get("size", 0),
                "avg_obj_size": stats.get("avgObjSize", 0),
                "storage_size": stats.get("storageSize", 0),
                "indexes": stats.get("nindexes", 0)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting collection stats: {str(e)}"
            }

# Create FastMCP server instance
server = FastMCP("mongodb-mcp-server")

# Create MongoDB server instance
mongo_server = MongoDBMCPServer()

@server.tool()
async def connect_to_mongodb_atlas(
    connection_string: str = Field(..., description="MongoDB Atlas connection string (mongodb+srv://username:password@cluster.mongodb.net/database)"),
    database_name: str = Field(..., description="Name of the database to connect to"),
    timeout_ms: int = Field(default=10000, description="Connection timeout in milliseconds (Atlas may need longer)"),
    use_ssl: bool = Field(default=True, description="Use SSL connection (recommended for Atlas)"),
    retry_writes: bool = Field(default=True, description="Enable retry writes for Atlas")
) -> Dict[str, Any]:
    """Connect to a MongoDB Atlas database"""
    config = MongoDBConfig(
        connection_string=connection_string,
        database_name=database_name,
        timeout_ms=timeout_ms,
        use_ssl=use_ssl,
        retry_writes=retry_writes
    )
    return await mongo_server.connect(config)

@server.tool()
async def list_collections() -> List[str]:
    """List all collections in the connected database"""
    return await mongo_server.list_collections()

@server.tool()
async def find_documents(
    collection_name: str = Field(..., description="Name of the collection to query"),
    query: Optional[Dict[str, Any]] = Field(default={}, description="MongoDB query filter (JSON object)"),
    limit: int = Field(default=100, description="Maximum number of documents to return"),
    sort_field: Optional[str] = Field(default=None, description="Field to sort by"),
    sort_direction: int = Field(default=1, description="Sort direction (1 for ascending, -1 for descending)")
) -> Dict[str, Any]:
    """Find documents in a MongoDB collection"""
    sort = None
    if sort_field:
        sort = [(sort_field, sort_direction)]
    
    params = CollectionQuery(
        collection_name=collection_name,
        query=query,
        limit=limit,
        sort=sort
    )
    return await mongo_server.find_documents(params)

@server.tool()
async def insert_document(
    collection_name: str = Field(..., description="Name of the collection to insert into"),
    document: Dict[str, Any] = Field(..., description="Document to insert (JSON object)")
) -> Dict[str, Any]:
    """Insert a document into a MongoDB collection"""
    params = DocumentInsert(
        collection_name=collection_name,
        document=document
    )
    return await mongo_server.insert_document(params)

@server.tool()
async def update_documents(
    collection_name: str = Field(..., description="Name of the collection to update"),
    query: Dict[str, Any] = Field(..., description="Query to find documents to update (JSON object)"),
    update: Dict[str, Any] = Field(..., description="Update operations (JSON object)"),
    upsert: bool = Field(default=False, description="Create document if it doesn't exist")
) -> Dict[str, Any]:
    """Update documents in a MongoDB collection"""
    params = DocumentUpdate(
        collection_name=collection_name,
        query=query,
        update=update,
        upsert=upsert
    )
    return await mongo_server.update_documents(params)

@server.tool()
async def delete_documents(
    collection_name: str = Field(..., description="Name of the collection to delete from"),
    query: Dict[str, Any] = Field(..., description="Query to find documents to delete (JSON object)")
) -> Dict[str, Any]:
    """Delete documents from a MongoDB collection"""
    params = DocumentDelete(
        collection_name=collection_name,
        query=query
    )
    return await mongo_server.delete_documents(params)

@server.tool()
async def get_collection_stats(
    collection_name: str = Field(..., description="Name of the collection to get stats for")
) -> Dict[str, Any]:
    """Get statistics for a MongoDB collection"""
    return await mongo_server.get_collection_stats(collection_name)

def main():
    """Main entry point for the MCP server"""
    print("🚀 Starting MongoDB Atlas MCP Server...")
    print("=" * 50)
    print("📋 Server Configuration:")
    print("  - FastMCP Framework")
    print("  - MongoDB Atlas Optimized")
    print("  - SSL/TLS Enabled")
    print("  - Retry Writes Enabled")
    print("=" * 50)
    print("🔌 Server is ready to accept MCP connections")
    print("Press Ctrl+C to stop the server")
    print("")
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    main() 