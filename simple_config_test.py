#!/usr/bin/env python3
"""
Simple configuration test without RAGFlow dependencies
"""
import yaml
import pymysql

def load_config():
    """Load and parse the service configuration"""
    try:
        with open('conf/service_conf.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return None

def test_mysql_connection(config):
    """Test MySQL connection with the loaded config"""
    mysql_config = config.get('mysql', {})
    
    connection_params = {
        'host': mysql_config.get('host'),
        'port': mysql_config.get('port', 3306),
        'user': mysql_config.get('user'),
        'password': mysql_config.get('password'),
        'database': mysql_config.get('name'),
        'connect_timeout': 10,
        'read_timeout': 10,
        'write_timeout': 10,
    }
    
    print("🔗 Testing MySQL Connection")
    print("Connection parameters:")
    for key, value in connection_params.items():
        if key == 'password':
            print(f"  {key}: {'*' * len(str(value)) if value else 'NOT SET'}")
        else:
            print(f"  {key}: {value}")
    
    try:
        connection = pymysql.connect(**connection_params)
        print("✅ Successfully connected to MySQL!")
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL Version: {version[0]}")
            
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            db_names = [db[0] for db in databases]
            print(f"✅ Available databases: {db_names}")
            
            if mysql_config.get('name') in db_names:
                print(f"✅ Target database '{mysql_config.get('name')}' exists")
            else:
                print(f"❌ Target database '{mysql_config.get('name')}' does not exist")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def main():
    print("🔍 Simple RAGFlow MySQL Configuration Test")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    print("✅ Configuration loaded successfully")
    
    # Test MySQL connection
    if test_mysql_connection(config):
        print("\n🎉 MySQL connection is working!")
        print("The issue might be with RAGFlow's internal connection handling.")
        print("\nSuggested fixes:")
        print("1. Check if all RAGFlow dependencies are installed")
        print("2. Verify RAGFlow is using the correct configuration file")
        print("3. Check for any connection pooling or timeout issues")
    else:
        print("\n❌ MySQL connection failed!")
        print("Please fix the connection issues before running RAGFlow.")

if __name__ == "__main__":
    main()
