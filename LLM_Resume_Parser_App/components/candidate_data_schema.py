from pydantic import BaseModel, Field
from typing import List, Optional


class date(BaseModel):
    """Date"""
    day: Optional[int] = Field(default=1,
                               description="Day of month, a integer from 1 and 31, if unkown the default is 1")
    month: Optional[int] = Field(description="Month of year, an integer from 1 to 12")
    year: Optional[int] = Field(description="Year in yyyy format")


class job(BaseModel):
    """Job details"""
    job_company: Optional[str] = Field(description="Name of the company")
    job_title: Optional[str] = Field(description="Job titile")
    job_description: Optional[str] = Field(
        description="Information about the job and what did the candidate do in it if available. Return all content provided.")
    started_at: Optional[date] = Field(
        description="what date did the candidate start this job? Return None if not available")
    ended_at: Optional[date] = Field(description="what date did the candidate end this job? Return None if not available")
    current_job: Optional[bool] = Field(
        description="True if this the candidates current job, False if it's not the candidate's current job")


class degree(BaseModel):
    """degree details, which only includes Bachelor's, Master's or Phd degrees"""
    degree_type: Optional[str] = Field(description="Degree type, which is Bachelor's, Master's or Phd")
    major: Optional[str] = Field(description="Degree major")
    university: Optional[str] = Field(description="Degree university")
    graduation_date: Optional[date] = Field(description="When did the candidate graduate or when will they graduate? Return None if not available")

class Project(BaseModel):
    """Model to represent a project with name and description."""
    name: Optional[str] = Field(description="Name of the project")
    description: Optional[str] = Field(description="Description of the project. Return all content provided, including tech stacks.")

class Activities_and_Certification(BaseModel):
    name: Optional[str] = Field(description="Name of the certification")
    organization: Optional[str] = Field(description="read name field to find out organization mentioned. Return null if not given")
    description: Optional[str] = Field(description="information about the certificate or activity or publications. Return null if not provided")


class candidate(BaseModel):
    """personal information about the candidate"""
    Activities_and_Certifications: Optional[list[Activities_and_Certification]] = Field(
        description="list of all candidates activities and certifications")
    projects: Optional[list[Project]] = Field(
        description="list of candidates projects that are listed. Return null if hasn't listed any")
    name: Optional[str] = Field(description="name")
    first_name: Optional[str] = Field(description="First name")
    last_name: Optional[str] = Field(description="Last name")
    country__phone_code: Optional[str] = Field(description="Country phone code, examples: +1 or +39")
    phone_number: Optional[int] = Field(description="Phone number, without country phone code")
    email: Optional[str] = Field(description="Email address")
    country: Optional[str] = Field(description="country")
    degrees: Optional[List[degree]] = Field(description="list of all candidate's degrees")
    jobs: Optional[List[job]] = Field(description="Only include jobs the candidate listed in a work experience section. Return None if he hasn't listed any.")
    skills: Optional[list[str]] = Field(description="list of candidate's skills that are relevant to the job")
    description: Optional[str] = Field(description="a short description or a autobiography of the candidate describing his qualities and proefessional goals. Return None if hasnt listed one")
    #links: Optional[list[Link]] = Field(description="list of candidate ocial media links such as twitter, linkedin, instagram or an url for a portfolio website. Return None if doesnt exist")
    linkedin: Optional[str] = Field(description="candidates linkedin handle web url. Return None if doesnt exist")
    instagram: Optional[str] = Field(description="candidates instagram handle web url. Return None if doesnt exist")
    twitter: Optional[str] = Field(description="candidates twitter handle web url. Return None if doesnt exist")
    portfolio: Optional[str] = Field(description="candidates portfolio website web url. Return None if doesnt exist")