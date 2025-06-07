from sqlalchemy import Column, Integer, String, Date, ARRAY
from sqlalchemy.sql import func
from database import Base 

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    core_skills = Column(ARRAY(String), nullable=False)
    soft_skills = Column(ARRAY(String), nullable=False)
    resume_rating = Column(Integer, nullable=False)
    improvement_areas = Column(String, nullable=False)
    upskill_suggestions = Column(String, nullable=False)
    file_location = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=func.current_date())