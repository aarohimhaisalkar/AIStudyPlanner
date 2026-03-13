"""
Fix PostgreSQL Setup Issues for Windows
"""

import subprocess
import sys
import os

def check_postgresql_service():
    """Check if PostgreSQL is running"""
    try:
        # Try to connect to PostgreSQL service
        result = subprocess.run(['sc', 'query', 'postgresql'], 
                              capture_output=True, text=True, shell=True)
        
        if 'RUNNING' in result.stdout:
            print("✅ PostgreSQL service is running")
            return True
        else:
            print("❌ PostgreSQL service is not running")
            return False
    except:
        print("⚠️ Could not check PostgreSQL service status")
        return False

def start_postgresql_service():
    """Start PostgreSQL service on Windows"""
    try:
        print("🚀 Starting PostgreSQL service...")
        result = subprocess.run(['sc', 'start', 'postgresql'], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("✅ PostgreSQL service started successfully")
            return True
        else:
            print(f"❌ Failed to start PostgreSQL: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error starting PostgreSQL: {e}")
        return False

def setup_postgres_password():
    """Reset PostgreSQL password for Windows setup"""
    print("🔧 Setting up PostgreSQL password...")
    
    try:
        # Connect to PostgreSQL as default user and set password
        commands = [
            # Connect to postgres database
            f'psql -U postgres -c "ALTER USER postgres PASSWORD \'newpassword123\';"',
            
            # Create study_planner user
            f'psql -U postgres -c "CREATE USER study_user WITH PASSWORD \'studypassword123\';"',
            
            # Create database
            f'psql -U postgres -c "CREATE DATABASE study_planner OWNER study_user;"',
            
            # Grant privileges
            f'psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE study_planner TO study_user;"'
        ]
        
        for cmd in commands:
            print(f"🔧 Executing: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️ Warning: {result.stderr}")
        
        print("✅ PostgreSQL setup completed!")
        print("📋 New credentials:")
        print("   Username: study_user")
        print("   Password: studypassword123")
        print("   Database: study_planner")
        
        # Update .env file
        update_env_file("postgresql://study_user:studypassword123@localhost:5432/study_planner")
        
    except Exception as e:
        print(f"❌ Error setting up PostgreSQL: {e}")

def update_env_file(database_url):
    """Update .env file with new DATABASE_URL"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace DATABASE_URL line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('DATABASE_URL='):
                lines[i] = f'DATABASE_URL={database_url}'
                break
        
        content = '\n'.join(lines)
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print(f"✅ Updated .env file with: {database_url}")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def main():
    print("🗄️ PostgreSQL Setup Fix Tool")
    print("=" * 50)
    
    # Check current status
    if not check_postgresql_service():
        print("\n🔧 Attempting to start PostgreSQL service...")
        if start_postgresql_service():
            print("⏳ Waiting for service to fully start...")
            import time
            time.sleep(3)
        else:
            print("❌ Could not start PostgreSQL service")
            print("🔧 Please install PostgreSQL from: https://www.postgresql.org/download/windows/")
            return
    
    print("\n🔧 Setting up database credentials...")
    setup_postgres_password()
    
    print("\n✅ Setup complete! You can now run:")
    print("   streamlit run app_db.py")

if __name__ == "__main__":
    main()
