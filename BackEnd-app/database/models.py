from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from AI import *

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
    title: str = None
    description: Optional[str] = None
    material_used: str
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
    title: str  
    description: Optional[str] = None  
    content_type: str  
    language: str  
    file_url: HttpUrl   
    uploaded_date: datetime = datetime.now()  # Date when the material was uploaded
    category: Optional[str] = None  # Category of the material (e.g., 'Mathematics', 'Physics', etc.)
    is_public: bool = True  # Whether the material is public or private
    


class Summary(BaseModel):
    material_id : str
    generated_summary : str
    detail_level : str

class FlashCard(BaseModel):
    flash_id : str



class ChatMessage(BaseModel):
    sender: str  # sys:0     user:1  
    message: str  # User's question or system's answer
    timestamp: datetime = datetime.now()  # Message timestamp


class ChatSession(BaseModel): 
    material_path: str  
 #   rag_model: RagChain
    chat_history: List[ChatMessage] = []  # List of messages in the chat
    created_at: datetime = datetime.now()
    last_active_at: datetime = datetime.now()
    

class IncomingChatMessage(BaseModel):
    chat_session_id : str
    message_content: str


    
