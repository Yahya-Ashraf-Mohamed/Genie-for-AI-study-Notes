from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime, timedelta

class User(BaseModel):
    username: str
    password: str
    isPremium: Optional[bool] = False
    email: EmailStr
    registrationDate: datetime = datetime.now()
    preferences: Optional[List[str]] = []
    studyGoals: Optional[str] = ""
    usageStats: Optional[dict] = {}
    progressReports: Optional[List[str]] = []


class Quiz(BaseModel):
    title: str
    description: Optional[str] = None
    creator: str
    creationDate: datetime = datetime.now()
    dueDate: datetime = datetime.now() + timedelta(days=7)
    questions: List[str]  
    answers: Optional[List[str]]    
    isPublic: bool
    category: Optional[str] = None
    maxAttempts: Optional[int] = None
    passingScore: Optional[float] = None
    feedback: Optional[dict] = None

class StudyMaterial(BaseModel):
    material_id: str  
    title: str  
    description: Optional[str] = None  
    content_type: str  
    language: str  
    file_url: HttpUrl   
    uploaded_date: datetime = datetime.now()  # Date when the material was uploaded
    category: Optional[str] = None  # Category of the material (e.g., 'Mathematics', 'Physics', etc.)
    is_public: bool = True  # Whether the material is public or private
    


class Summary(BaseModel):
    Summary_id : str
    material_id : str
    content : str
    detail_level : str

class FlashCard(BaseModel):
    flash_id : str
    
