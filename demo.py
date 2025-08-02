#!/usr/bin/env python3
"""
Demo script for Masari Learning Platform
Shows how to use the application programmatically
"""

import requests
import json
from app import app, db
from app.models.models import Users, LearningPaths, Courses, Lessons
from app.services.llm_service import llm_service

def demo_llm_service():
    """Demo the LLM service"""
    print("🤖 Demo: LLM Service")
    print("-" * 30)
    
    # Test learning path generation
    prompt = "Create a learning path for JavaScript programming"
    print(f"Prompt: {prompt}")
    response = llm_service.generate_response(prompt)
    print(f"Response: {response}")
    print()

def demo_database_operations():
    """Demo database operations"""
    print("🗄️  Demo: Database Operations")
    print("-" * 30)
    
    with app.app_context():
        # Create a test user
        from app import bcrypt
        hashed_password = bcrypt.generate_password_hash('test123').decode('utf-8')
        
        # Check if test user exists
        test_user = Users.query.filter_by(username='demo_user').first()
        if not test_user:
            test_user = Users(
                username='demo_user',
                password=hashed_password,
                name='Demo User',
                birthdate=None
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Created demo user")
        else:
            print("✅ Demo user already exists")
        
        # Create a test learning path
        test_path = LearningPaths.query.filter_by(title='Demo Learning Path').first()
        if not test_path:
            test_path = LearningPaths(
                title='Demo Learning Path',
                user_id=test_user.id
            )
            db.session.add(test_path)
            db.session.commit()
            print("✅ Created demo learning path")
        else:
            print("✅ Demo learning path already exists")
        
        # Create a test course
        test_course = Courses.query.filter_by(title='Demo Course').first()
        if not test_course:
            test_course = Courses(
                title='Demo Course',
                learning_path_id=test_path.id,
                user_id=test_user.id
            )
            db.session.add(test_course)
            db.session.commit()
            print("✅ Created demo course")
        else:
            print("✅ Demo course already exists")
        
        # Create a test lesson
        test_lesson = Lessons.query.filter_by(title='Demo Lesson').first()
        if not test_lesson:
            test_lesson = Lessons(
                title='Demo Lesson',
                course_id=test_course.id,
                content='This is a demo lesson content.'
            )
            db.session.add(test_lesson)
            db.session.commit()
            print("✅ Created demo lesson")
        else:
            print("✅ Demo lesson already exists")
        
        print(f"📊 Database contains:")
        print(f"   - {Users.query.count()} users")
        print(f"   - {LearningPaths.query.count()} learning paths")
        print(f"   - {Courses.query.count()} courses")
        print(f"   - {Lessons.query.count()} lessons")
        print()

def demo_api_endpoints():
    """Demo API endpoints"""
    print("🌐 Demo: API Endpoints")
    print("-" * 30)
    
    base_url = "http://localhost:5000"
    
    # Note: These would require authentication in a real scenario
    print("Available API endpoints:")
    print("  POST /api/generate_learningpath - Generate learning path")
    print("  POST /api/generate_lessons - Generate lessons")
    print("  POST /api/generate_content - Generate lesson content")
    print("  POST /api/generate_reply - Get AI responses")
    print("  POST /api/mark_completed - Mark lesson completed")
    print()

def main():
    """Main demo function"""
    print("🎓 Masari Learning Platform - Demo")
    print("=" * 50)
    
    # Demo LLM service
    demo_llm_service()
    
    # Demo database operations
    demo_database_operations()
    
    # Demo API endpoints
    demo_api_endpoints()
    
    print("🎉 Demo completed!")
    print("\n📋 To run the full application:")
    print("1. python start.py")
    print("2. Open http://localhost:5000")
    print("3. Register a new account")
    print("4. Create your first learning path!")

if __name__ == '__main__':
    main() 