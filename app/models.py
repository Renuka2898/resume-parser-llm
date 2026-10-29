"""Validated resume output models."""
from pydantic import BaseModel, Field

class ContactInformation(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None

class WorkExperience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    responsibilities: list[str] = Field(default_factory=list)

class Education(BaseModel):
    degree: str | None = None
    institution: str | None = None
    year: str | None = None

class ResumeData(BaseModel):
    contact_information: ContactInformation = Field(default_factory=ContactInformation)
    professional_summary: str | None = None
    work_experience: list[WorkExperience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    technical_skills: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

class UploadResponse(BaseModel):
    document_id: str
    resume: ResumeData
