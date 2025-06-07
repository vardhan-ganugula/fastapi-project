from fastapi import FastAPI, Request, File, UploadFile, Depends,Form
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse 
from pydantic import BaseModel
import time 
import model 
from database import engine, SessionLocal 
from sqlalchemy.orm import Session
from local_types import ResumeAnalysis
from langchain_analysis import get_analysis

app = FastAPI()
model.Base.metadata.create_all(bind=engine)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request,
    })

@app.get('/upload')
def upload(request: Request):
    return templates.TemplateResponse('upload.html', {
        'request': request
    }) 

@app.post('/upload')
async def upload_file(title: str = Form(...), resume: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await resume.read()
    currentTime = str(time.time() * 1000)
    file_location = f'./static/files/{currentTime}-{resume.filename}'
    with open(file_location, 'wb') as f:
        f.write(contents)
    response_data : ResumeAnalysis = get_analysis(file_location, role=title)
    for key, value in response_data.dict().items():
        if type(value) == str and "Error" in value:
            return {"status": 'error', "message": value}
    db_resume = model.Resume(
        name=response_data.name,
        email=response_data.email,
        core_skills=response_data.core_skills,
        soft_skills=response_data.soft_skills,
        resume_rating=response_data.resume_rating,
        improvement_areas=response_data.improvement_areas,
        upskill_suggestions=response_data.upskill_suggestions,
        file_location=file_location
    )
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    return {"status": 'success', "data": response_data} 


@app.get('/history')
async def history(request: Request, db:Session = Depends(get_db)):
    resume = db.query(model.Resume).all()
    return templates.TemplateResponse('history.html', {
        'request': request,
        'resumes': resume
    })
