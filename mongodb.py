# mongodb.py
from pymongo import MongoClient

# Initialize MongoDB client and database
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ai_study_assistant"]
generated_content = mongo_db["generated_content"]

# Function to insert generated content into MongoDB
def insert_generated_content(material_id: str, summary: str, questions: list, answers: list):
    """Insert generated content (summary, questions, answers) into MongoDB"""
    content = {
        "material_id": material_id,  # Link to the study material in PostgreSQL
        "summary": summary,
        "questions": questions,
        "answers": answers
    }
    generated_content.insert_one(content)
