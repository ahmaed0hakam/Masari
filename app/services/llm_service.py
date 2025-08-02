import requests
import json
from typing import Optional
from config.config import Config

class LLMService:
    """
    Service for interacting with free online LLMs
    Currently using HuggingFace Inference API with a free model
    """
    
    def __init__(self):
        # Using HuggingFace Inference API with a free model
        # You can get a free API key from https://huggingface.co/settings/tokens
        self.api_url = f"https://api-inference.huggingface.co/models/{Config.HUGGINGFACE_MODEL}"
        self.headers = {
            "Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}"
        }
        
        # Fallback to a simple text generation service if HuggingFace is not available
        self.fallback_url = "https://api.text-generator.io/v1/generate"
    
    def generate_response(self, prompt: str, max_length: int = 500) -> str:
        """
        Generate a response using the LLM service
        
        Args:
            prompt (str): The input prompt
            max_length (int): Maximum length of the response
            
        Returns:
            str: Generated response
        """
        try:
            # Try HuggingFace API first
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    return result.get('generated_text', '')
            
            # Fallback to simple text generation
            return self._fallback_generate(prompt, max_length)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._fallback_generate(prompt, max_length)
    
    def _fallback_generate(self, prompt: str, max_length: int) -> str:
        """
        Fallback method using a simple text generation approach
        """
        try:
            # Simple rule-based response generation for common patterns
            if "learning path" in prompt.lower():
                return self._generate_learning_path_response(prompt)
            elif "lesson" in prompt.lower():
                return self._generate_lesson_response(prompt)
            elif "course" in prompt.lower():
                return self._generate_course_response(prompt)
            else:
                return self._generate_generic_response(prompt)
        except Exception as e:
            print(f"Fallback generation error: {e}")
            return "I'm sorry, I couldn't generate a response at the moment."
    
    def _generate_learning_path_response(self, prompt: str) -> str:
        """Generate a learning path response"""
        # Extract topic from prompt
        topic = self._extract_topic(prompt)
        
        courses = [
            f"1. Introduction to {topic}",
            f"2. Fundamentals of {topic}",
            f"3. Advanced {topic} Concepts",
            f"4. {topic} Best Practices",
            f"5. {topic} Project Implementation"
        ]
        
        return "\n".join(courses)
    
    def _generate_lesson_response(self, prompt: str) -> str:
        """Generate lesson content"""
        topic = self._extract_topic(prompt)
        
        return f"""
# {topic}

## Overview
This lesson covers the essential concepts of {topic}.

## Key Topics
1. Basic concepts and terminology
2. Core principles and methodologies
3. Practical applications and examples

## Exercises
- Practice exercises to reinforce learning
- Real-world examples and case studies
- Hands-on projects and assignments

## Summary
A comprehensive overview of {topic} with practical applications.
        """
    
    def _generate_course_response(self, prompt: str) -> str:
        """Generate course structure"""
        topic = self._extract_topic(prompt)
        
        lessons = [
            f"1. Introduction to {topic}",
            f"2. Core Concepts of {topic}",
            f"3. Advanced {topic} Techniques",
            f"4. {topic} in Practice",
            f"5. Final Project and Assessment"
        ]
        
        return "\n".join(lessons)
    
    def _generate_generic_response(self, prompt: str) -> str:
        """Generate a generic response"""
        return "I understand your question. Here's a helpful response based on the available information."
    
    def _extract_topic(self, prompt: str) -> str:
        """Extract the main topic from the prompt"""
        # Simple topic extraction
        words = prompt.split()
        for i, word in enumerate(words):
            if word.lower() in ['for', 'about', 'in', 'of'] and i + 1 < len(words):
                return words[i + 1].capitalize()
        return "the subject"

# Global instance
llm_service = LLMService() 