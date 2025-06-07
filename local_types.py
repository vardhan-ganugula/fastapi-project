from pydantic import BaseModel, Field
from typing import List


class ResumeAnalysis(BaseModel):
    """Pydantic model for structured resume analysis output"""
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address of the candidate")
    core_skills: List[str] = Field(description="Technical/hard skills relevant to the role")
    soft_skills: List[str] = Field(description="Interpersonal and behavioral skills")
    resume_rating: int = Field(description="Overall resume rating out of 100", ge=1, le=100)
    improvement_areas: str = Field(description="Areas that need improvement")
    upskill_suggestions: str = Field(description="Specific skills to develop for the role")
