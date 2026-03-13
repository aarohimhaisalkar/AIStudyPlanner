"""
PostgreSQL Database Setup Script for AI Study Planner
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    
    # Connect to PostgreSQL server (default database)
    db_name = "study_planner"
    user = "postgres"
    password = "password"  # Change this to your PostgreSQL password
    host = "localhost"
    port = "5432"
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            dbname="postgres",  # Default database
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' created successfully!")
        else:
            print(f"ℹ️ Database '{db_name}' already exists.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print("🔧 Make sure PostgreSQL is running and your credentials are correct")
        return False
    
    return True

def setup_database_url():
    """Help user set up their DATABASE_URL"""
    
    print("🗄️ PostgreSQL Database Setup for AI Study Planner")
    print("=" * 50)
    
    # Get user input
    print("\n📝 Please enter your PostgreSQL details:")
    
    username = input("Username (default: postgres): ").strip() or "postgres"
    password = input("Password: ").strip()
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = input("Port (default: 5432): ").strip() or "5432"
    database = input("Database name (default: study_planner): ").strip() or "study_planner"
    
    # Construct DATABASE_URL
    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    print(f"\n🔗 Your DATABASE_URL:")
    print(database_url)
    
    # Update .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace or add DATABASE_URL
        if 'DATABASE_URL=' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('DATABASE_URL='):
                    lines[i] = f'DATABASE_URL={database_url}'
            content = '\n'.join(lines)
        else:
            content += f'\nDATABASE_URL={database_url}'
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print(f"\n✅ DATABASE_URL updated in .env file!")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        print("🔧 Please manually update your .env file with:")
        print(f"DATABASE_URL={database_url}")

def test_connection():
    """Test database connection"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Successfully connected to PostgreSQL!")
        print(f"📊 Database version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ AI Study Planner - Database Setup")
    print("=" * 50)
    
    choice = input("""
Choose an option:
1. Create database
2. Set up DATABASE_URL
3. Test connection
4. Exit

Enter choice (1-4): """).strip()
    
    if choice == "1":
        create_database()
    elif choice == "2":
        setup_database_url()
    elif choice == "3":
        test_connection()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please try again.")
