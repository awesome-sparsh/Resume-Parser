from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from components.utils import extract_resume_text, convert_dates_to_datetime, is_valid_email
from components.llm_resume_parser import llm_resume_parser
from datetime import datetime, date

import io

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class CandidateData(BaseModel):
    parsed_candidate_data: dict


def calculate_duration(start_date_str=None, end_date_str=None):
    # Define the date format
    date_format = "%Y-%m-%d"
    
    # If start_date_str is None, return 0
    if start_date_str is None:
        return 0

    # Convert start_date_str to a date object if it's a string
    if isinstance(start_date_str, str):
        start_date = datetime.strptime(start_date_str, date_format).date()
    elif isinstance(start_date_str, date):
        start_date = start_date_str
    else:
        raise ValueError("start_date_str must be a string, date object, or None")

    # If end_date_str is None, use today's date
    if end_date_str is None:
        end_date = date.today()
    else:
        # Convert end_date_str to a date object if it's a string
        if isinstance(end_date_str, str):
            end_date = datetime.strptime(end_date_str, date_format).date()
        elif isinstance(end_date_str, date):
            end_date = end_date_str
        else:
            raise ValueError("end_date_str must be a string or a date object")

    # Calculate the total number of months between start_date and end_date
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    # If the end day is before the start day, adjust the month difference
    if end_date.day < start_date.day:
        total_months -= 1

    return total_months


@app.post("/upload_resume", response_model=CandidateData)
async def upload_resume(
        resume: UploadFile = File(...),
        job_title: Optional[str] = Form(None)
):
    if not resume:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Read file content and determine file type
    file_content = await resume.read()
    file_type = resume.filename.split(".")[-1].lower()

    try:
        # Pass file_content and file_type to extract_resume_text
        resume_text = await extract_resume_text(file_content, file_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract resume text: {str(e)}")

    try:
        parsed_candidate_data = llm_resume_parser.invoke({"job_title": job_title, "resume_text": resume_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    candidate_data = convert_dates_to_datetime(parsed_candidate_data)

    if 'email' in candidate_data and not is_valid_email(candidate_data['email']):
        candidate_data['email'] = ''
#    candidate_data['degrees'][0]['sparsh']='heloo'

    if 'phone_number' in candidate_data and candidate_data['phone_number']!=None:
        phone=candidate_data['phone_number']
        candidate_data['phone_number']=str(phone)


    total_job_experience=0
    if candidate_data['jobs']:
        for job in candidate_data['jobs']:
            start=job['started_at']
            end=job['ended_at']
            total_job_experience+=calculate_duration(start, end)
        candidate_data["total_job_experience_months"]=str(total_job_experience)
        total_job_experience_years = round(total_job_experience / 12)
        total_job_experience_years = int(total_job_experience_years)
        candidate_data["total_job_experience_years"] = str(total_job_experience_years)




    return CandidateData(parsed_candidate_data=candidate_data)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
