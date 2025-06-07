import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from local_types import ResumeAnalysis
import json
import re
import os
import extraction
from dotenv import load_dotenv 

load_dotenv()


class ResumeOutputParser(BaseOutputParser):
    """Custom parser to extract structured data from LLM response"""
    
    def parse(self, text: str) -> ResumeAnalysis:
        try:
            
            # Clean the response text
            cleaned_text = text.strip()
            
            # Try to extract JSON from the response - more flexible regex
            json_patterns = [
                r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested JSON
                r'\{.*?\}',  # Simple JSON
                r'```json\s*(\{.*?\})\s*```',  # JSON in code blocks
            ]
            
            for pattern in json_patterns:
                json_match = re.search(pattern, cleaned_text, re.DOTALL | re.IGNORECASE)
                if json_match:
                    json_str = json_match.group(1) if len(json_match.groups()) > 0 else json_match.group(0)
                    try:
                        data = json.loads(json_str)
                        
                        # Validate required fields
                        required_fields = ['name', 'email', 'core_skills', 'soft_skills', 'resume_rating', 'improvement_areas', 'upskill_suggestions']
                        if all(field in data for field in required_fields):
                            return ResumeAnalysis(**data)
                    except json.JSONDecodeError as je:
                        print(f"JSON decode error: {je}")
                        continue
            
            # If no valid JSON found, try fallback parsing
            return self._fallback_parse(cleaned_text)
            
        except Exception as e:
            return self._fallback_parse(text)
    
    def _fallback_parse(self, text: str) -> ResumeAnalysis:
        """Fallback method to parse non-JSON responses"""
        lines = text.split('\n')
        data = {
            'name': 'Not Found',
            'email': 'Not Found',
            'core_skills': [],
            'soft_skills': [],
            'resume_rating': 5,
            'improvement_areas': 'Unable to parse response properly',
            'upskill_suggestions': 'Unable to parse response properly'
        }
        
        # Try to extract information from structured text
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip().strip('"').strip("'")
                
                if 'name' in key:
                    data['name'] = value
                elif 'email' in key:
                    data['email'] = value
                elif 'rating' in key:
                    rating_match = re.search(r'\d+', value)
                    if rating_match:
                        data['resume_rating'] = min(100, max(1, int(rating_match.group())))
                elif 'improvement' in key:
                    data['improvement_areas'] = value
                elif 'upskill' in key or 'suggestion' in key:
                    data['upskill_suggestions'] = value
        
        return ResumeAnalysis(**data)


class ResumeAnalyzer:
    """Resume analyzer using Google Gemini AI with LangChain"""
    
    def __init__(self, api_key: str | None = None):
        """Initialize the resume analyzer"""
        if api_key:
            genai.configure(api_key=api_key)
        else:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("Google AI API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # Using more stable model
        self.output_parser = ResumeOutputParser()
        
        # Improved prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["resume_text", "role"],
            template="""You are a strict HR professional analyzing a resume for the {role} position.

RESUME TEXT:
{resume_text}

Analyze this resume and respond ONLY with a valid JSON object in this exact format:

{{
    "name": "candidate full name or 'Not Found'",
    "email": "email address or 'Not Found'", 
    "core_skills": ["technical skill 1", "technical skill 2"],
    "soft_skills": ["soft skill 1", "soft skill 2"],
    "resume_rating": 45,
    "improvement_areas": "specific areas needing improvement",
    "upskill_suggestions": "specific skills to develop for {role}"
}}

STRICT EVALUATION RULES:
- Rating scale: 1-100 (most resumes score 40-80 for average candidates and having relevent skills , 80-100 for exceptional candidates, 1-30 for poor resumes)
- Only list skills explicitly mentioned in the resume
- Be critical about gaps and missing achievements
- Focus on relevance to {role} position

RESPOND WITH ONLY THE JSON OBJECT - NO OTHER TEXT:"""
        )
    
    def analyze_resume(self, resume_text: str, role: str) -> ResumeAnalysis:
        """Analyze a resume for a specific role"""
        try:
            # Validate inputs
            if not resume_text or not resume_text.strip():
                raise ValueError("Resume text is empty or invalid")
            
            if len(resume_text.strip()) < 50:
                raise ValueError("Resume text too short - possible extraction error")
            
            
            # Format the prompt
            formatted_prompt = self.prompt_template.format(
                resume_text=resume_text[:4000],  # Limit text length to avoid token limits
                role=role
            )
            
            # Generate response using Gemini
            response = self.model.generate_content(
                formatted_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # Lower temperature for more consistent JSON output
                    top_p=0.8,

                )
            )
            
            if not response.text:
                raise ValueError("Empty response from Gemini AI")
            
            # Parse the response
            analysis = self.output_parser.parse(response.text)
            return analysis
            
        except Exception as e:
            # Return structured error response
            return ResumeAnalysis(
                name="Analysis Error",
                email="Analysis Error", 
                core_skills=["Error in analysis"],
                soft_skills=["Error in analysis"],
                resume_rating=1,
                improvement_areas=f"Analysis failed: {str(e)}",
                upskill_suggestions="Please check resume file and try again"
            )


def get_analysis(location: str, role: str) -> ResumeAnalysis:
    """Get resume analysis from file location"""
    try:
        # Extract text from PDF/document
        resume_text = extraction.extract_text_from_pdf(location)
        # Validate extracted text
        if not resume_text or len(resume_text.strip()) < 10:
            return ResumeAnalysis(
                name="Extraction Error",
                email="Extraction Error",
                core_skills=["Text extraction failed"],
                soft_skills=["Text extraction failed"], 
                resume_rating=1,
                improvement_areas="Could not extract text from the uploaded file",
                upskill_suggestions="Please upload a valid PDF or document file"
            )
        
        
        # Analyze the resume
        analyzer = ResumeAnalyzer()
        return analyzer.analyze_resume(resume_text, role)
        
    except Exception as e:
        print(f"get_analysis error: {str(e)}")
        return ResumeAnalysis(
            name="System Error",
            email="System Error",
            core_skills=["System error occurred"],
            soft_skills=["System error occurred"],
            resume_rating=1,
            improvement_areas=f"System error: {str(e)}",
            upskill_suggestions="Please contact support"
        )