# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required for the API endpoints.

## Endpoints

### 1. Home Page
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns the main landing page
- **Response**: HTML page

### 2. Upload Form Page
- **URL**: `/upload`
- **Method**: `GET`
- **Description**: Returns the resume upload form
- **Response**: HTML page with upload form

### 3. Process Resume Upload
- **URL**: `/upload`
- **Method**: `POST`
- **Description**: Uploads and analyzes a PDF resume
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `title` (form field, required): The job role/position for analysis
  - `resume` (file, required): PDF file containing the resume

#### Success Response
```json
{
  "status": "success",
  "data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "core_skills": ["Python", "FastAPI", "PostgreSQL", "Machine Learning"],
    "soft_skills": ["Communication", "Leadership", "Problem Solving"],
    "resume_rating": 85,
    "improvement_areas": "Consider adding more specific project outcomes and quantifiable achievements. Include relevant certifications or training programs.",
    "upskill_suggestions": "Consider learning cloud technologies like AWS or Azure, and modern DevOps practices to enhance your profile."
  }
}
```

#### Error Response
```json
{
  "status": "error",
  "message": "Error description here"
}
```

### 4. Resume History
- **URL**: `/history`
- **Method**: `GET`
- **Description**: Returns a page displaying all previously analyzed resumes
- **Response**: HTML page with resume history table

## Data Models

### ResumeAnalysis
The structured response model for resume analysis:

```python
{
  "name": str,                    # Full name of the candidate
  "email": str,                   # Email address
  "core_skills": List[str],       # Technical/hard skills
  "soft_skills": List[str],       # Interpersonal skills
  "resume_rating": int,           # Rating from 1-100
  "improvement_areas": str,       # Areas needing improvement
  "upskill_suggestions": str      # Skills to develop
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server-side error

Common error scenarios:
- Invalid file format (non-PDF files)
- Missing required form fields
- AI analysis failures
- Database connection issues

## Rate Limiting
Currently, no rate limiting is implemented.

## Examples

### cURL Example
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "title=Software Engineer" \
  -F "resume=@/path/to/resume.pdf"
```

### Python Example
```python
import requests

url = "http://localhost:8000/upload"
files = {"resume": open("resume.pdf", "rb")}
data = {"title": "Software Engineer"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### JavaScript Example
```javascript
const formData = new FormData();
formData.append('title', 'Software Engineer');
formData.append('resume', fileInput.files[0]);

fetch('/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Response Time
Typical response times:
- Upload and analysis: 5-15 seconds (depends on resume complexity)
- Page loads: < 1 second
- History retrieval: < 2 seconds
