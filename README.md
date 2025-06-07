# Resume Processor - AI-Powered Resume Analysis System

A FastAPI-based web application that analyzes resumes using AI to extract key information, provide ratings, and suggest improvements.

## 🚀 Features

- **PDF Resume Upload**: Upload and process PDF resumes
- **AI-Powered Analysis**: Uses Google's Generative AI to analyze resumes
- **Structured Data Extraction**: Extracts candidate information, skills, and provides ratings
- **Database Storage**: Stores analysis results in PostgreSQL database
- **Web Interface**: Modern, responsive web interface with Tailwind CSS
- **History Management**: View all previously analyzed resumes

## 📋 Table of Contents

- [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Contributing](#contributing)

## 📸 Screenshots

### Home Page
The main landing page with navigation options and clean interface.

![Home Page](screenshots/Screenshot%20(86).png)

### Resume Upload Interface
Upload form where users can select PDF resumes and specify the job role for analysis.

![Upload Interface](screenshots/Screenshot%20(87).png)

### Analysis Results
Detailed analysis results showing extracted information, skills, ratings, and improvement suggestions.

![Analysis Results](screenshots/Screenshot%20(88).png)

### Resume History
View all previously analyzed resumes with their details and ratings.

![Resume History](screenshots/Screenshot%20(89).png)

> 📝 **Note**: For detailed descriptions of each interface and feature, see [SCREENSHOTS.md](SCREENSHOTS.md)

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Google AI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vardhan-ganugula/fastapi-project
   cd "fastapi-project"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   POSTGRES_URL=postgresql://username:password@localhost:5432/resume_db
   GOOGLE_API_KEY=your_google_ai_api_key
   ```

5. **Set up database**
   - Create a PostgreSQL database named `resume_db`
   - The application will automatically create the required tables

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_URL` | PostgreSQL connection string | `postgresql://postgres:vardhan@localhost:5432/resume_db` |
| `GOOGLE_API_KEY` | Google AI API key for resume analysis | Required |

### Database Configuration

The application uses PostgreSQL with SQLAlchemy ORM. The database schema is automatically created when the application starts.

## 🚀 Usage

### Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn app:app --reload
   ```

2. **Access the application**
   - Web Interface: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Using the Web Interface

1. **Home Page** (`/`): Landing page with navigation options
2. **Upload Resume** (`/upload`): Upload PDF resumes for analysis
3. **View History** (`/history`): View all previously analyzed resumes

### API Usage

The application provides RESTful API endpoints for integration with other systems.

## 📖 API Endpoints

### GET Endpoints

| Endpoint | Description | Response |
|----------|-------------|----------|
| `/` | Home page | HTML template |
| `/upload` | Upload form page | HTML template |
| `/history` | View all analyzed resumes | HTML template with resume list |

### POST Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/upload` | POST | Upload and analyze resume | `title` (str), `resume` (file) |

#### Upload Resume Response

```json
{
  "status": "success",
  "data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "core_skills": ["Python", "FastAPI", "PostgreSQL"],
    "soft_skills": ["Communication", "Leadership"],
    "resume_rating": 85,
    "improvement_areas": "Add more project details",
    "upskill_suggestions": "Learn cloud technologies"
  }
}
```

## 🗄️ Database Schema

### Resume Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `name` | STRING | Candidate's full name |
| `email` | STRING | Candidate's email address |
| `core_skills` | ARRAY(STRING) | Technical/hard skills |
| `soft_skills` | ARRAY(STRING) | Interpersonal skills |
| `resume_rating` | INTEGER | Rating out of 100 |
| `improvement_areas` | STRING | Areas needing improvement |
| `upskill_suggestions` | STRING | Recommended skills to learn |
| `file_location` | STRING | Path to uploaded PDF file |
| `created_at` | DATE | Record creation date |

## 🏗️ Architecture

### Core Components

1. **FastAPI Application** (`app.py`)
   - Main web server and API endpoints
   - Request handling and response formatting
   - Database integration

2. **Database Layer** (`database.py`, `model.py`)
   - PostgreSQL connection management
   - SQLAlchemy ORM models
   - Database session handling

3. **AI Analysis Engine** (`langchain_analysis.py`)
   - Google Generative AI integration
   - Resume text analysis and parsing
   - Structured data extraction

4. **PDF Processing** (`extraction.py`)
   - PDF text extraction using PyMuPDF
   - File validation and error handling

5. **Data Models** (`local_types.py`)
   - Pydantic models for data validation
   - Type definitions for API responses

### Data Flow

1. User uploads PDF resume via web interface
2. PDF text is extracted using PyMuPDF
3. Text is analyzed using Google's Generative AI
4. AI response is parsed into structured data
5. Data is stored in PostgreSQL database
6. Results are returned to user

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation and parsing
- **PyMuPDF**: PDF text extraction

### AI/ML
- **Google Generative AI**: Resume analysis
- **LangChain**: AI application framework

### Frontend
- **Jinja2**: Template engine
- **Tailwind CSS**: Utility-first CSS framework
- **HTML5**: Markup language

### Development
- **python-dotenv**: Environment variable management
- **uvicorn**: ASGI server

## 📁 File Structure

```
fastapi project/
├── README.md             # Main project documentation
├── SETUP_GUIDE.md        # Detailed setup instructions
├── API_DOCUMENTATION.md  # API reference guide
├── DEPLOYMENT_GUIDE.md   # Production deployment guide
├── ARCHITECTURE.md       # Technical architecture docs
├── SCREENSHOTS.md        # Interface screenshots and descriptions
├── app.py                # Main FastAPI application
├── database.py           # Database configuration
├── model.py              # SQLAlchemy models
├── langchain_analysis.py # AI analysis engine
├── extraction.py         # PDF text extraction
├── local_types.py        # Pydantic data models
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── screenshots/          # Application interface screenshots
│   ├── Screenshot (86).png  # Home page
│   ├── Screenshot (87).png  # Upload interface
│   ├── Screenshot (88).png  # Analysis results
│   └── Screenshot (89).png  # Resume history
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── files/          # Uploaded resume files
├── templates/           # HTML templates
│   ├── index.html      # Home page
│   ├── upload.html     # Upload form
│   └── history.html    # Resume history
└── __pycache__/        # Python cache files
```

## 🔧 Development

### Adding New Features

1. **New API Endpoints**: Add to `app.py`
2. **Database Changes**: Modify `model.py` and run migrations
3. **AI Analysis**: Update `langchain_analysis.py`
4. **Frontend**: Add templates and static files

### Testing

Run the application in development mode:
```bash
uvicorn app:app --reload
```

### Code Quality

- Follow PEP 8 style guide
- Use type hints
- Add docstrings to functions
- Handle exceptions appropriately

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Include error messages and logs if applicable

## 📈 Future Enhancements

- [ ] Support for multiple file formats (DOC, DOCX)
- [ ] Batch processing capabilities
- [ ] Advanced analytics and reporting
- [ ] User authentication and authorization
- [ ] Resume comparison features
- [ ] Export functionality (PDF, Excel)
- [ ] RESTful API versioning
- [ ] Docker containerization
- [ ] Unit and integration tests
