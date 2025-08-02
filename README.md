# Masari Learning Platform

A Flask-based learning platform that uses AI to generate personalized learning paths and content. The project has been reorganized with a clean architecture and uses free online LLM services.

## 🏗️ Project Structure

```
masari/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/
│   │   └── models.py            # Database models
│   ├── routes/
│   │   ├── auth.py              # Authentication routes
│   │   ├── main.py              # Main application routes
│   │   └── api.py               # API endpoints
│   ├── forms/
│   │   └── forms.py             # Flask-WTF forms
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py      # LLM service layer
│   ├── utils/
│   │   └── helpers.py           # Utility functions
│   ├── static/                  # Static files (CSS, JS, images)
│   └── templates/               # HTML templates
├── config/
│   └── config.py                # Configuration settings
├── CVs/                         # Upload directory for CVs
├── requirements.txt              # Python dependencies
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization
├── setup.py                     # Automated setup script
├── start.py                     # Comprehensive start script
├── test_llm.py                  # LLM service testing
├── demo.py                      # Demo script
└── README.md                    # This file
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd masari
   ```

2. **Run the automated setup:**
   ```bash
   python3 setup.py
   ```

3. **Get a free HuggingFace API key:**
   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
   - Create a new token
   - Update the `HUGGINGFACE_API_KEY` in the `.env` file

4. **Initialize the database:**
   ```bash
   python3 init_db.py
   ```

5. **Run the application:**
   ```bash
   python3 run.py
   ```

6. **Open your browser:**
   Navigate to `http://localhost:5000`

### Option 2: Manual Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` (if available)
   - Add your HuggingFace API key to the `.env` file

4. **Initialize the database:**
   ```bash
   python3 init_db.py
   ```

5. **Run the application:**
   ```bash
   python3 run.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Get your free HuggingFace API key from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=hf_your_api_key_here

# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
```

### LLM Service Configuration

The application uses a free online LLM service with fallback options:

- **Primary**: HuggingFace Inference API (free tier available)
- **Fallback**: Rule-based text generation for basic functionality

## 🎯 Features

- **User Authentication**: Register, login, and logout functionality
- **Personalized Learning Paths**: AI-generated learning paths based on user interests
- **Dynamic Content Generation**: AI-powered course and lesson content
- **Progress Tracking**: Mark lessons as completed
- **Interactive Learning**: AI assistant for answering questions
- **CV Upload**: Support for PDF, DOC, and DOCX files
- **Responsive Design**: Modern web interface

## 📚 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Learning Paths
- `POST /api/generate_learningpath` - Generate a new learning path
- `GET /learningpath/<id>` - View learning path details

### Courses and Lessons
- `POST /api/generate_lessons` - Generate lessons for a course
- `POST /api/generate_content` - Generate content for a lesson
- `GET /course/<id>/<title>` - View course details

### Interactive Features
- `POST /api/generate_reply` - Get AI responses to questions
- `POST /api/mark_completed` - Mark lesson as completed

## 🔐 Demo Account

A demo account has been created for testing:

- **Username**: `demo`
- **Password**: `demo123`

You can use this account to test the application without registering.

## 🛠️ Development

### Project Architecture

The project follows a clean architecture pattern:

- **Routes**: Handle HTTP requests and responses
- **Services**: Business logic and external API interactions
- **Models**: Database models and relationships
- **Forms**: Input validation and form handling
- **Utils**: Helper functions and utilities

### Adding New Features

1. **Database Models**: Add to `app/models/models.py`
2. **Routes**: Add to appropriate route file in `app/routes/`
3. **Services**: Add business logic to `app/services/`
4. **Forms**: Add form classes to `app/forms/forms.py`

### Database Migrations

To modify the database schema:

1. Update the models in `app/models/models.py`
2. Delete the existing `database.db` file
3. Run `python3 init_db.py` to recreate the database

## 🧪 Testing

### Test the LLM Service
```bash
python3 test_llm.py
```

### Run the Demo
```bash
python3 demo.py
```

### Comprehensive Start
```bash
python3 start.py
```

## 🔍 Troubleshooting

### Common Issues

1. **LLM Service Not Working**
   - Check your HuggingFace API key in `.env`
   - Verify internet connection
   - The application will fall back to rule-based generation

2. **Database Errors**
   - Run `python3 init_db.py` to recreate the database
   - Check file permissions for the `instance/` directory

3. **Import Errors**
   - Ensure you're in the virtual environment
   - Run `pip install -r requirements.txt`

4. **Port Already in Use**
   - Change the port in `config/config.py`
   - Or kill the process using the port: `lsof -ti:5000 | xargs kill -9`

5. **Template Not Found**
   - Ensure templates are in the `templates/` directory
   - Check Flask app configuration in `app/__init__.py`

## 📦 Dependencies

### Core Dependencies
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling
- **Flask-Bcrypt**: Password hashing
- **Flask-CORS**: Cross-origin resource sharing

### AI/ML Dependencies
- **requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management

### File Processing
- **pdfplumber**: PDF text extraction

## 🎓 How to Use

### 1. Register/Login
- Go to `http://localhost:5000`
- Click "Register" to create a new account
- Or use the demo account (username: `demo`, password: `demo123`)

### 2. Create Learning Paths
- After logging in, you'll see the dashboard
- Click "Create New Learning Path"
- Enter a topic (e.g., "Python Programming", "Web Development")
- The AI will generate a personalized learning path

### 3. Explore Courses
- Click on any learning path to see its courses
- Each course contains multiple lessons
- The AI generates course content dynamically

### 4. Complete Lessons
- Click on any lesson to view its content
- Mark lessons as completed to track progress
- Ask questions using the AI assistant

### 5. AI Features
- **Learning Path Generation**: AI creates personalized learning paths
- **Course Generation**: AI generates course structures
- **Lesson Content**: AI creates detailed lesson content
- **Q&A Assistant**: Ask questions about lessons

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- HuggingFace for providing free AI model access
- Flask community for the excellent web framework
- All contributors to the open-source dependencies

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the logs in the `logs/` directory
3. Create an issue on the project repository
4. Contact the development team

## 🔄 Recent Changes

### Project Reorganization
- ✅ Split monolithic `app.py` into organized modules
- ✅ Created service layer for LLM operations
- ✅ Implemented free online LLM service (HuggingFace)
- ✅ Added comprehensive setup and testing scripts
- ✅ Improved error handling and fallback mechanisms
- ✅ Enhanced documentation and user guides

### LLM Service Updates
- ✅ Replaced Ollama with free HuggingFace API
- ✅ Added fallback rule-based generation
- ✅ Improved prompt engineering
- ✅ Enhanced error handling

---

**Happy Learning! 🎓**

*The application is now running successfully with a clean, organized architecture and free AI capabilities!*