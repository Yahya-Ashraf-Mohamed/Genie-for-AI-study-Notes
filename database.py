# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (replace with your own PostgreSQL connection string)
DATABASE_URL = "postgresql://assistant_user:newpassword@localhost/ai_study_assistant"


# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Define the StudyMaterial model
class StudyMaterial(Base):
    __tablename__ = 'study_materials'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content_type = Column(String)

# Create tables in the database
Base.metadata.create_all(bind=engine)
