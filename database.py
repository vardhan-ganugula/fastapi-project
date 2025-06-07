from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
from dotenv import load_dotenv
load_dotenv()
import os
URL_DATABASE = os.getenv('POSTGRES_URL', 'postgresql://postgres:vardhan@localhost:5432/resume_db')

engine = create_engine(URL_DATABASE) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
