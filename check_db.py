#!/usr/bin/env python3
"""Check database contents"""

import sqlite3
import os

db_path = 'study_planner.db'

if os.path.exists(db_path):
    print(f"✅ Database file exists: {db_path}")
    print(f"📁 File size: {os.path.getsize(db_path)} bytes")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tables in database: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📋 {table_name}: {count} records")
            
            # Show sample data if table has records
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                print(f"    📝 Sample data: {sample_data}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")
else:
    print(f"❌ Database file not found: {db_path}")
