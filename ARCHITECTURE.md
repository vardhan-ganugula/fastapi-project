# Technical Architecture Documentation

## System Overview

The Resume Processor is a web-based application that analyzes PDF resumes using AI technology. The system extracts structured information from resumes, provides ratings and improvement suggestions, and stores the results in a database for future reference.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   FastAPI App   │    │   PostgreSQL    │
│                 │    │                 │    │   Database      │
│  - HTML/CSS/JS  │◄──►│  - API Routes   │◄──►│                 │
│  - File Upload  │    │  - Business     │    │  - Resume Data  │
│  - Result View  │    │    Logic        │    │  - History      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Google AI     │
                       │   Generative    │
                       │   API           │
                       └─────────────────┘
```

## Component Architecture

### 1. Web Layer (Presentation Tier)

#### Frontend Components
- **Templates**: Jinja2 HTML templates with embedded data
- **Static Assets**: CSS (Tailwind), JavaScript, uploaded files
- **Responsive Design**: Mobile-friendly interface

#### Key Files:
- `templates/index.html` - Landing page
- `templates/upload.html` - Resume upload form
- `templates/history.html` - Analysis history
- `static/js/script.js` - Client-side interactions

### 2. Application Layer (Business Logic Tier)

#### FastAPI Application (`app.py`)
```python
# Core responsibilities:
- HTTP request/response handling
- Route definitions and middleware
- Form data processing
- Template rendering
- Database session management
```

#### Key Routes:
- `GET /` - Home page
- `GET /upload` - Upload form
- `POST /upload` - Process resume upload
- `GET /history` - View analysis history

### 3. Service Layer

#### AI Analysis Service (`langchain_analysis.py`)
```python
# Core responsibilities:
- Resume text analysis using Google AI
- Response parsing and validation
- Error handling and fallback logic
- Structured data extraction
```

#### PDF Processing Service (`extraction.py`)
```python
# Core responsibilities:
- PDF text extraction using PyMuPDF
- File validation
- Error handling for corrupted files
```

### 4. Data Layer (Persistence Tier)

#### Database Models (`model.py`)
```python
class Resume(Base):
    # Stores structured resume analysis results
    - Personal information (name, email)
    - Skills categorization (core, soft)
    - Analysis results (rating, suggestions)
    - File metadata (location, timestamp)
```

#### Database Configuration (`database.py`)
```python
# Database connection management:
- SQLAlchemy engine configuration
- Session management
- Connection pooling
```

### 5. Data Models (`local_types.py`)

#### Pydantic Models
```python
class ResumeAnalysis(BaseModel):
    # Data validation and serialization
    - Type checking and validation
    - API response structure
    - Documentation generation
```

## Data Flow Architecture

### 1. Resume Upload Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Browser   │    │  FastAPI    │    │   File      │
│             │    │             │    │   System    │
│ 1. Upload   │───►│ 2. Receive  │───►│ 3. Save     │
│    PDF      │    │    File     │    │    PDF      │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Database  │    │  Analysis   │    │   PDF       │
│             │    │  Service    │    │ Processor   │
│ 6. Store    │◄───│ 5. Parse    │◄───│ 4. Extract  │
│   Results   │    │   Response  │    │    Text     │
└─────────────┘    └─────────────┘    └─────────────┘
                           ▲
                           │
                    ┌─────────────┐
                    │  Google AI  │
                    │             │
                    │ 5. Analyze  │
                    │   Resume    │
                    └─────────────┘
```

### 2. Data Processing Pipeline

```
Raw PDF File
     │
     ▼
Text Extraction (PyMuPDF)
     │
     ▼
AI Analysis (Google Generative AI)
     │
     ▼
Response Parsing (Custom Parser)
     │
     ▼
Data Validation (Pydantic)
     │
     ▼
Database Storage (SQLAlchemy)
     │
     ▼
User Response (JSON/HTML)
```

## Technology Stack

### Backend Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Framework | FastAPI | API development, request handling |
| Database ORM | SQLAlchemy | Database abstraction, model definition |
| Database | PostgreSQL | Data persistence, relational storage |
| PDF Processing | PyMuPDF | Text extraction from PDF files |
| AI/ML | Google Generative AI | Resume analysis and insights |
| Data Validation | Pydantic | Type checking, API documentation |
| Template Engine | Jinja2 | HTML template rendering |
| Environment Config | python-dotenv | Configuration management |

### Frontend Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| CSS Framework | Tailwind CSS | Styling and responsive design |
| JavaScript | Vanilla JS | Client-side interactions |
| HTML | HTML5 | Structure and semantics |

## Database Schema Design

### Tables

#### `resumes` Table
```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    core_skills TEXT[] NOT NULL,
    soft_skills TEXT[] NOT NULL,
    resume_rating INTEGER NOT NULL CHECK (resume_rating >= 1 AND resume_rating <= 100),
    improvement_areas TEXT NOT NULL,
    upskill_suggestions TEXT NOT NULL,
    file_location VARCHAR NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);
```

#### Indexes
```sql
CREATE INDEX idx_resumes_created_at ON resumes(created_at);
CREATE INDEX idx_resumes_rating ON resumes(resume_rating);
CREATE INDEX idx_resumes_email ON resumes(email);
```

## API Design

### RESTful Principles
- Clear resource naming
- HTTP status codes for responses
- Consistent error handling
- JSON response format

### Request/Response Format

#### Upload Request
```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data

title: Software Engineer
resume: [PDF file data]
```

#### Success Response
```json
{
  "status": "success",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "core_skills": ["Python", "FastAPI"],
    "soft_skills": ["Communication"],
    "resume_rating": 85,
    "improvement_areas": "...",
    "upskill_suggestions": "..."
  }
}
```

## Security Architecture

### Data Protection
- Environment variable isolation
- Secure file storage
- Database connection encryption
- Input validation and sanitization

### API Security
- File type validation
- File size limitations
- Rate limiting considerations
- Error message sanitization

### File System Security
- Uploaded files stored outside web root
- Unique file naming to prevent conflicts
- File access permission restrictions

## Error Handling Strategy

### Error Categories

1. **User Errors** (400-level)
   - Invalid file format
   - Missing required fields
   - File too large

2. **System Errors** (500-level)
   - Database connection failures
   - AI API failures
   - File system errors

### Error Response Format
```json
{
  "status": "error",
  "message": "Human-readable error description",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Performance Considerations

### Bottlenecks and Optimizations

1. **AI API Calls**
   - Longest operation (5-15 seconds)
   - Implement timeout handling
   - Consider caching for similar resumes

2. **PDF Processing**
   - Memory usage for large files
   - File size limitations
   - Concurrent processing limits

3. **Database Operations**
   - Connection pooling
   - Query optimization
   - Index usage

### Scaling Strategies

#### Horizontal Scaling
- Stateless application design
- Database connection pooling
- Load balancer compatible

#### Vertical Scaling
- Memory optimization for PDF processing
- CPU optimization for AI processing
- Storage optimization for file uploads

## Monitoring and Observability

### Logging Strategy
```python
# Log levels:
- ERROR: System failures, exceptions
- WARNING: Recoverable errors, performance issues
- INFO: Request processing, business events
- DEBUG: Detailed troubleshooting information
```

### Metrics to Monitor
- Request response times
- AI API call latency
- Database query performance
- File upload success rates
- Error rates by category

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": check_database_connection(),
        "ai_service": check_ai_service(),
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Development Patterns

### Dependency Injection
FastAPI's dependency injection system for:
- Database session management
- Configuration injection
- Service layer dependencies

### Error Handling Patterns
```python
try:
    # Process resume
    result = process_resume(file)
except PDFProcessingError as e:
    return {"status": "error", "message": str(e)}
except AIServiceError as e:
    return {"status": "error", "message": "Analysis failed"}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"status": "error", "message": "Internal server error"}
```

### Configuration Management
```python
# Environment-based configuration
class Settings:
    database_url: str = Field(..., env="POSTGRES_URL")
    ai_api_key: str = Field(..., env="GOOGLE_API_KEY")
    debug: bool = Field(False, env="DEBUG")
```

## Future Architecture Enhancements

### Planned Improvements

1. **Microservices Architecture**
   - Separate AI processing service
   - File storage service
   - User management service

2. **Caching Layer**
   - Redis for session management
   - Response caching for similar resumes
   - File metadata caching

3. **Message Queue**
   - Asynchronous resume processing
   - Background job processing
   - Scalable AI analysis

4. **API Versioning**
   - Version-specific endpoints
   - Backward compatibility
   - Progressive enhancement

### Containerization
```dockerfile
# Multi-stage build for optimization
FROM python:3.12-slim AS builder
# Build dependencies

FROM python:3.12-slim AS runtime
# Runtime environment
```

## Testing Strategy

### Test Pyramid

1. **Unit Tests**
   - Individual function testing
   - Data model validation
   - Business logic verification

2. **Integration Tests**
   - Database operations
   - API endpoint testing
   - Service integration

3. **End-to-End Tests**
   - Complete user workflows
   - UI interaction testing
   - Performance testing

### Test Coverage Areas
- PDF text extraction accuracy
- AI response parsing reliability
- Database CRUD operations
- API endpoint functionality
- Error handling robustness
