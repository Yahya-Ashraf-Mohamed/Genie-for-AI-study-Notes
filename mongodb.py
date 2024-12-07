from pymongo import MongoClient

# Use the provided MongoDB Atlas URI
uri = "mongodb+srv://moustafatoofii:<QVvp@riy6.2KJ8b>@sw.rhyx7.mongodb.net/?retryWrites=true&w=majority&appName=sw"

# Initialize MongoDB client and database
mongo_client = MongoClient(uri)
mongo_db = mongo_client["ai_study_assistant"]
generated_content = mongo_db["generated_content"]

# Function to insert generated content into MongoDB
def insert_generated_content(material_id: str, summary: str, questions: list, answers: list):
    """Insert generated content (summary, questions, answers) into MongoDB"""
    content = {
        "material_id": material_id,
        "summary": summary,
        "questions": questions,
        "answers": answers
    }
    generated_content.insert_one(content)
