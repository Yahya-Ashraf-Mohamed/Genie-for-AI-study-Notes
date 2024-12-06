from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient



# MongoDB connection URL
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ai_study_assistant"]
generated_content = mongo_db["generated_content"]

# You can insert a document into the collection like this:
content = {
    "material_id": "some_id",  # this will be linked to the PostgreSQL record
    "summary": "Sample summary...",
    "questions": ["What is AI?", "Define NLP."],
    "answers": ["AI is...", "NLP stands for..."]
}
generated_content.insert_one(content)


# Database URL for PostgreSQL (you might need to adjust the username, password, and host)
SQLALCHEMY_DATABASE_URL = "postgresql://assistant_user:securepassword@localhost/ai_study_assistant"

# Create a database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Define your database models
class StudyMaterial(Base):
    __tablename__ = 'study_materials'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content_type = Column(String)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
