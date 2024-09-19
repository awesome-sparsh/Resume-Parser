import PyPDF2
import docx
import io
import datetime
from components.candidate_data_schema import candidate
import re
import aiofiles
from PyPDF2 import PdfReader
from dateutil import parser
from datetime import date


def read_pdf_text(file_content):
    """
    Extracts text from a PDF file.

    Args:
        file_content (bytes): The PDF file content.

    Returns:
        str: The extracted text from the PDF.
    """
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text().strip()
    return text


def read_docx_text(file_content):
    """
    Extracts text from a DOCX file.

    Args:
        file_content (bytes): The DOCX file content.

    Returns:
        str: The extracted text from the DOCX file.
    """
    doc = docx.Document(io.BytesIO(file_content))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text.strip() + "\n"
    return text


async def extract_resume_text(file_content, file_type):
    """
    Extracts text from a resume file based on its type.

    Args:
        file_content (bytes): The file content.
        file_type (str): The type of the file ('pdf', 'doc', 'docx', 'txt', or 'text').

    Returns:
        str: The extracted text from the file.
    """
    if file_type == "pdf":
        return read_pdf_text(file_content)
    elif file_type in ["doc", "docx"]:
        return read_docx_text(file_content)
    elif file_type in ["txt", "text"]:
        async with aiofiles.BytesIO(file_content) as file:
            return await file.read()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def date_to_datetime(input):
    # If the input is a string, handle it differently
    if isinstance(input, str):
        try:
            # Try to parse the string into a date object using dateutil parser
            parsed_date = parser.parse(input)
            return date(parsed_date.year, parsed_date.month, parsed_date.day)
        except ValueError:
            # Handle cases like "Present"
            if input.lower() == "present":
                return None  # Or handle it according to your logic
            raise ValueError(f"Cannot parse date string: {input}")

    # If input is a dictionary-like object, proceed with conversion
    if isinstance(input, dict):
        year = input.get("year")
        month = input.get("month", 1)
        day = input.get("day", 1)
        if year:
            try:
                if day is None:
                    day = 1
                if month is None:
                    month = 1
                if year is None:
                    year = 1
                if year is None and month is None and day is None:
                    return "null"
                return date(year, month, day)

            except:
                return
        else:
            return None
    raise ValueError(f"Invalid input for date conversion: {input}")

def convert_dates_to_datetime(candidate_data: candidate):
    """
    Returns the model_dump() dictionary of a "candidate" pydantic class after converting dates to datetime.date objects.

    Args:
        candidate_data (candidate): The candidate object containing date fields.

    Returns:
        dict: The candidate model_dump dictionary with date fields converted to datetime.date objects.
    """
    candidate_dict = candidate_data.model_dump()

    if "degrees" in candidate_dict.keys():
        for degree in candidate_dict["degrees"]:
            if degree["graduation_date"]:
                degree["graduation_date"] = date_to_datetime(degree["graduation_date"])

    if candidate_dict["jobs"]:
        for job in candidate_dict["jobs"]:
            if job["started_at"]:
                if not date_to_datetime(job["started_at"]):
                    job["started_at"]=None
                else:
                    job["started_at"] = date_to_datetime(job["started_at"])
            if job["ended_at"]:
                job["ended_at"] = date_to_datetime(job["ended_at"])

    return candidate_dict


def is_valid_email(email):
    """
    Checks if an email address is valid.

    Args:
        email (str): The email address.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
