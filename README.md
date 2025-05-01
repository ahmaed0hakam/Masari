# Masari Learning Platform

A Flask-based learning platform that uses AI to generate personalized learning paths and content.

## Project Structure

```
masari/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── api.py
│   ├── forms/
│   │   └── forms.py
│   ├── utils/
│   │   └── helpers.py
│   ├── static/
│   └── templates/
├── config/
│   └── config.py
├── CVs/
├── requirements.txt
├── run.py
└── README.md
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have Ollama installed and running with the llama3 model:
   ```bash
   ollama run llama3
   ```

4. Initialize the database:
   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. Run the application:
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## Features

- User authentication (register/login)
- Personalized learning paths generation
- Course and lesson generation using AI
- Interactive content generation
- Progress tracking
- CV upload and processing
- API endpoints for dynamic content generation

## Dependencies

- Flask and its extensions (SQLAlchemy, Login, WTF, Bcrypt, CORS)
- Langchain for AI integration
- PDFPlumber for CV processing
- Ollama as the LLM provider

## API Endpoints

- `/api/generate_learningpath` - Generate a new learning path
- `/api/generate_lessons` - Generate lessons for a course
- `/api/generate_content` - Generate content for a lesson
- `/api/generate_reply` - Generate AI responses to user questions
- `/api/mark_completed` - Mark a lesson as completed

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request