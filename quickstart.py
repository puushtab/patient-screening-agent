#!/usr/bin/env python3
"""
MongoDB Atlas MCP Server - Quick Start
Simple script to get you up and running quickly
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    print("✅ requirements.txt found")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment...")
    
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env.example"):
        # Copy env.example to .env
        with open("env.example", "r") as src:
            content = src.read()
        
        with open(".env", "w") as dst:
            dst.write(content)
        
        print("✅ Created .env file from template")
        print("\n⚠️  IMPORTANT: You need to edit .env with your MongoDB Atlas details:")
        print("   1. Replace 'username:password' with your Atlas credentials")
        print("   2. Replace 'cluster.mongodb.net' with your cluster URL")
        print("   3. Replace 'database' with your database name")
        print("\n📖 See README.md for detailed Atlas setup instructions")
        return False  # Need manual configuration
    else:
        print("❌ env.example not found")
        return False

def test_connection():
    """Test Atlas connection"""
    print("\n🧪 Testing MongoDB Atlas connection...")
    
    if not os.path.exists("test_atlas_connection.py"):
        print("⚠️  Connection test script not found, skipping test")
        return True
    
    try:
        result = subprocess.run([sys.executable, "test_atlas_connection.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Atlas connection test passed")
            return True
        else:
            print("❌ Atlas connection test failed")
            print("Please check your .env configuration")
            return False
    except Exception as e:
        print(f"❌ Error running connection test: {e}")
        return False

def start_server():
    """Start the MCP server"""
    print("\n🚀 Starting MongoDB Atlas MCP Server...")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the server
        from mongo_mcp_server import main
        main()
    except ImportError as e:
        print(f"❌ Failed to import server: {e}")
        print("Make sure all dependencies are installed")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main quickstart function"""
    print("🎯 MongoDB Atlas MCP Server - Quick Start")
    print("=" * 50)
    
    # Step 1: Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 3: Setup environment
    env_ready = setup_environment()
    
    if not env_ready:
        print("\n🔄 Please edit the .env file and run this script again")
        sys.exit(0)
    
    # Step 4: Test connection
    if not test_connection():
        print("\n🔄 Please fix the connection issues and run this script again")
        sys.exit(1)
    
    # Step 5: Start server
    start_server()

if __name__ == "__main__":
    main() 