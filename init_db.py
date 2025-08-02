#!/usr/bin/env python3
"""
Database initialization script for Masari Learning Platform
"""

from app import app, db
from app.models.models import Users, LearningPaths, Courses, Lessons

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if tables were created (using inspect instead of table_names)
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Created tables: {', '.join(tables)}")

if __name__ == '__main__':
    print("🚀 Initializing Masari Learning Platform Database...")
    init_database()
    print("✅ Database initialization complete!") 