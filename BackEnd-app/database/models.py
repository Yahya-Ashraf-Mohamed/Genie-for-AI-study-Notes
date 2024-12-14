from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime, timedelta

class User(BaseModel):
    username: str
    password: str
    isPremium: Optional [bool] = False
    email: EmailStr  
    registrationDate: datetime  = datetime.timestamp(datetime.now())
    preferences: Optional[List[str]] = None 
    studyGoals: Optional[str] = None        
    usageStats: Optional[dict] = None       
    progressReports: Optional[List[str]] = None 

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
    material_id : str
    title : str
    content_type : str
    language : str


class Summary(BaseModel):
    Summary_id : str
    material_id : str
    content : str
    detail_level : str

class FlashCard(BaseModel):
    flash_id : str
    
