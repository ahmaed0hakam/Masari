#!/usr/bin/env python3
"""
Test script for the LLM service
"""

from app.services.llm_service import llm_service

def test_llm_service():
    """Test the LLM service with various prompts"""
    
    print("🧪 Testing LLM Service...")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Learning Path Generation",
            "prompt": "Create a learning path for Python programming",
            "expected_type": "learning path"
        },
        {
            "name": "Lesson Content Generation",
            "prompt": "Generate lesson content for Introduction to Python",
            "expected_type": "lesson"
        },
        {
            "name": "Course Structure Generation",
            "prompt": "Create course structure for Web Development",
            "expected_type": "course"
        },
        {
            "name": "Generic Response",
            "prompt": "What is machine learning?",
            "expected_type": "generic"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print(f"Prompt: {test_case['prompt']}")
        
        try:
            response = llm_service.generate_response(test_case['prompt'])
            print(f"✅ Response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 LLM Service test completed!")

if __name__ == '__main__':
    test_llm_service() 