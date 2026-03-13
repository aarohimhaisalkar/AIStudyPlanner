# 🗄️ PostgreSQL Setup Guide for AI Study Planner

## 📋 Prerequisites

1. **Install PostgreSQL**
   ```bash
   # Windows
   # Download from: https://www.postgresql.org/download/windows/
   
   # macOS
   brew install postgresql
   
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Setup (3 Methods)

### Method 1: Automatic Setup Script
```bash
python setup_database.py
```
Follow the prompts to configure your database.

### Method 2: Manual Local Setup

1. **Start PostgreSQL Service**
   ```bash
   # Windows
   net start postgresql
   
   # macOS/Linux
   sudo systemctl start postgresql
   ```

2. **Create Database**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # In psql shell:
   CREATE DATABASE study_planner;
   CREATE USER study_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE study_planner TO study_user;
   \q
   ```

3. **Update .env File**
   ```env
   DATABASE_URL=postgresql://study_user:your_password@localhost:5432/study_planner
   ```

### Method 3: Cloud Database (Recommended)

#### Option A: Supabase (Free & Easy)
1. Go to [https://supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings → Database
4. Copy connection string
5. Update .env file:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

#### Option B: Railway (Simple)
1. Go to [https://railway.app](https://railway.app)
2. Create new project → Add PostgreSQL
3. Get connection string
4. Update .env file

#### Option C: ElephantSQL (Affordable)
1. Go to [https://elephantsql.com](https://elephantsql.com)
2. Create new database
3. Get connection details
4. Update .env file

## 🔧 Configuration

### Update Your .env File
```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# PostgreSQL Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/study_planner
```

## 🚀 Run Application

### With Database
```bash
# Use the enhanced database version
streamlit run app_db.py
```

### Without Database (Original)
```bash
# Use the original file-based version
streamlit run app.py
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preferences TEXT
);
```

### Study Plans Table
```sql
CREATE TABLE study_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan_name VARCHAR(100) NOT NULL,
    subjects TEXT NOT NULL,
    daily_hours FLOAT NOT NULL,
    sleep_hours FLOAT NOT NULL,
    meal_time FLOAT NOT NULL,
    play_time FLOAT NOT NULL,
    exercise_time FLOAT NOT NULL,
    personal_time FLOAT NOT NULL,
    screen_time_limit FLOAT NOT NULL,
    plan_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Progress Table
```sql
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan_id INTEGER REFERENCES study_plans(id),
    task_id VARCHAR(100) NOT NULL,
    task_description TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completion_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Features

### ✅ What You Get:
- **👤 User Accounts**: Login/registration system
- **💾 Persistent Storage**: Study plans saved in database
- **📊 Progress Tracking**: Real-time progress updates
- **🔄 Data Sync**: Access from anywhere
- **📈 Analytics**: Advanced progress analytics
- **🔒 Security**: User authentication
- **📱 Multi-device**: Same account across devices

### 🎯 Enhanced Functionality:
- **Study Plan History**: All your plans saved
- **Progress Analytics**: Detailed completion stats
- **Cross-session Sync**: Progress preserved
- **User Preferences**: Personalized settings
- **Data Backup**: Database-level backups

## 🛠️ Troubleshooting

### Common Issues:

#### Connection Error
```bash
❌ Error: could not connect to server
```
**Solution:**
1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify credentials in .env file
3. Check firewall settings

#### Database Doesn't Exist
```bash
❌ Error: database "study_planner" does not exist
```
**Solution:**
1. Run: `python setup_database.py`
2. Choose option 1 to create database

#### Permission Denied
```bash
❌ Error: permission denied for database study_planner
```
**Solution:**
1. Grant permissions: `GRANT ALL PRIVILEGES ON DATABASE study_planner TO your_user;`
2. Check user credentials

## 🚀 Production Deployment

### Environment Variables
Set these in your hosting environment:
- `DATABASE_URL`
- `OPENAI_API_KEY`

### Recommended Hosting:
1. **Supabase** - Free PostgreSQL hosting
2. **Railway** - Simple deployment
3. **Heroku** - Popular choice
4. **AWS RDS** - Enterprise solution

## 📞 Support

If you encounter issues:
1. Check PostgreSQL service status
2. Verify .env configuration
3. Test connection: `python setup_database.py`
4. Review logs for detailed errors

---

**🎉 Your AI Study Planner now has full PostgreSQL database integration!**
