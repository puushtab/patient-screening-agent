#!/bin/bash

# MongoDB Atlas MCP Server Startup Script

echo "🚀 Starting MongoDB Atlas MCP Server..."
echo "======================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from template."
        echo "🔧 Please edit .env with your MongoDB Atlas connection details:"
        echo "   1. Set your Atlas connection string"
        echo "   2. Set your database name"
        echo "   3. Save the file and run this script again"
        exit 1
    else
        echo "❌ env.example not found. Please create a .env file manually."
        exit 1
    fi
fi

# Test Atlas connection first
echo "🧪 Testing MongoDB Atlas connection..."
python3 test_atlas_connection.py

if [ $? -ne 0 ]; then
    echo "❌ Atlas connection test failed. Please fix the connection issues first."
    exit 1
fi

# Start the server
echo ""
echo "🔌 Starting MongoDB Atlas MCP Server..."
echo "Press Ctrl+C to stop the server"
echo ""

python3 mongo_mcp_server.py 