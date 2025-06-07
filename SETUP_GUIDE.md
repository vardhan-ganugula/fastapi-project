# Setup Guide

This guide will help you set up and run the Resume Processor application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher**
- **PostgreSQL 12 or higher**
- **Git** (for cloning the repository)
- **Google AI API Key** (for resume analysis)

## Step-by-Step Setup

### 1. Clone or Download the Project

If using Git:
```bash
git clone <repository-url>
cd "fastapi project"
```

Or download and extract the project files to your desired directory.

### 2. Set Up Python Environment

#### Create Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database

#### Install PostgreSQL
- Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
- During installation, remember the password you set for the `postgres` user

#### Create Database
Open PostgreSQL command line (psql) or use pgAdmin:

```sql
-- Connect as postgres user
CREATE DATABASE resume_db;

-- Optional: Create a dedicated user
CREATE USER resume_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE resume_db TO resume_user;
```

### 4. Get Google AI API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API key"
4. Create a new API key
5. Copy the API key for use in the next step

### 5. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
# Database Configuration
POSTGRES_URL=postgresql://postgres:your_password@localhost:5432/resume_db

# Google AI Configuration
GOOGLE_API_KEY=your_google_ai_api_key_here
```

**Important**: Replace the placeholders with your actual values:
- `your_password`: Your PostgreSQL password
- `your_google_ai_api_key_here`: Your Google AI API key

### 6. Initialize Database Tables

The application will automatically create the required database tables when it starts for the first time.

### 7. Create Required Directories

The application expects certain directories to exist:

```bash
mkdir -p static/files
mkdir -p static/css
mkdir -p static/js
```

### 8. Run the Application

Start the FastAPI development server:

```bash
uvicorn app:app --reload
```

You should see output similar to:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReloader
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 9. Access the Application

Open your web browser and navigate to:
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Verification

To verify everything is working correctly:

1. **Database Connection**: Check the console for any database connection errors

2. **Upload Test**: Try uploading a sample PDF resume
   - Navigate to the upload page
   - Select a PDF file and enter a job title
   - Verify the analysis results are displayed

3. **History Page**: Check if the history page loads without errors

### Expected Results

If everything is set up correctly, you should see:

#### Home Page
![Home Page](screenshots/Screenshot%20(86).png)

#### Upload Interface
![Upload Interface](screenshots/Screenshot%20(87).png)

#### Analysis Results
![Analysis Results](screenshots/Screenshot%20(88).png)

#### Resume History
![Resume History](screenshots/Screenshot%20(89).png)

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed
```

**Solutions:**
- Ensure PostgreSQL is running
- Check your database URL in the `.env` file
- Verify the database exists
- Check username/password

#### 2. Google AI API Error
```
google.api_core.exceptions.Unauthenticated: 401 Request had invalid authentication credentials
```

**Solutions:**
- Verify your Google AI API key is correct
- Ensure the API key is properly set in the `.env` file
- Check if your API key has the necessary permissions

#### 3. Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
- Ensure your virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version compatibility

#### 4. PDF Processing Error
```
RuntimeError: An error occurred while extracting text from the PDF
```

**Solutions:**
- Ensure the uploaded file is a valid PDF
- Check file permissions
- Try with a different PDF file

#### 5. Port Already in Use
```
ERROR: [Errno 10048] Only one usage of each socket address is normally permitted
```

**Solutions:**
- Stop any other applications using port 8000
- Use a different port: `uvicorn app:app --port 8001 --reload`
- Kill the process using the port

### Getting Help

If you encounter issues not covered here:

1. Check the application logs in the terminal
2. Verify all prerequisites are installed correctly
3. Ensure all environment variables are set properly
4. Try running with debug mode: `uvicorn app:app --reload --log-level debug`

## Development Setup

For development purposes, you may want to:

### Enable Debug Mode
Add to your `.env` file:
```env
DEBUG=True
```

### Use Development Database
Consider using a separate database for development:
```env
POSTGRES_URL=postgresql://postgres:password@localhost:5432/resume_db_dev
```

### Auto-reload Configuration
The `--reload` flag automatically restarts the server when code changes are detected.

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use production database and API keys
2. **WSGI Server**: Use Gunicorn instead of Uvicorn for production
3. **Reverse Proxy**: Set up Nginx as a reverse proxy
4. **SSL Certificate**: Configure HTTPS
5. **Database Migration**: Use Alembic for database migrations
6. **Logging**: Configure proper logging
7. **Monitoring**: Set up application monitoring

## Next Steps

Once you have the application running:

1. Explore the web interface
2. Test the API endpoints using the documentation
3. Upload sample resumes to test functionality
4. Review the code structure and architecture
5. Consider customizing the analysis prompts for your needs
