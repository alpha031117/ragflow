#!/usr/bin/env python3
"""
Debug script to test database configuration loading
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_config_loading():
    """Test how RAGFlow loads database configuration"""
    try:
        from api.utils import get_base_config, decrypt_database_config
        
        print("🔍 Testing Database Configuration Loading")
        print("=" * 50)
        
        # Test basic config loading
        print("1. Loading raw MySQL config...")
        mysql_config = get_base_config("mysql", {})
        print(f"Raw config: {mysql_config}")
        
        # Test decrypted config loading (this is what RAGFlow uses)
        print("\n2. Loading decrypted MySQL config...")
        decrypted_config = decrypt_database_config(name="mysql")
        print(f"Decrypted config: {decrypted_config}")
        
        # Test database connection parameters
        print("\n3. Database connection parameters:")
        print(f"  Host: {decrypted_config.get('host', 'NOT SET')}")
        print(f"  Port: {decrypted_config.get('port', 'NOT SET')}")
        print(f"  Database: {decrypted_config.get('name', 'NOT SET')}")
        print(f"  User: {decrypted_config.get('user', 'NOT SET')}")
        print(f"  Password: {'*' * len(str(decrypted_config.get('password', '')))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test actual database connection using RAGFlow's method"""
    try:
        print("\n🔗 Testing Database Connection")
        print("=" * 30)
        
        from api import settings
        from api.db.db_models import BaseDataBase
        
        print(f"Database type: {settings.DATABASE_TYPE}")
        print(f"Database config: {settings.DATABASE}")
        
        # Try to create database connection
        db_instance = BaseDataBase()
        print("✅ Database connection object created successfully")
        
        # Test connection
        db_connection = db_instance.database_connection
        print(f"Connection object: {type(db_connection)}")
        
        # Try to connect
        db_connection.connect()
        print("✅ Database connection established!")
        
        # Test simple query
        cursor = db_connection.execute_sql("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✅ Test query result: {result}")
        
        db_connection.close()
        print("✅ Database connection closed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🐛 RAGFlow Database Configuration Debug")
    print("=" * 60)
    
    # Test configuration loading
    config_ok = test_config_loading()
    
    if config_ok:
        # Test database connection
        connection_ok = test_database_connection()
        
        if connection_ok:
            print("\n🎉 All tests passed! Database is ready for RAGFlow.")
        else:
            print("\n❌ Database connection failed. Check the error details above.")
    else:
        print("\n❌ Configuration loading failed. Check your conf/service_conf.yaml file.")

if __name__ == "__main__":
    main()
