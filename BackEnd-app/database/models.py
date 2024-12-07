from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime, timedelta

class User(BaseModel):
    username: str
    password: str
    isPremium: bool
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
