from datetime import datetime
from database.schemas import get_chat_session
from config import *

def mongo_to_dict(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

def save_chat_session(session_id: str, material_id: str, chat_history: list):
    """
    Inserts a new chat session or updates an existing one in the database.
    """
    chat_sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "material_id": material_id,
                "chat_history": chat_history,
                "updated_at": datetime.now()
            }
        },
        upsert=True  # Insert the document if it doesn't exist
    )

def get_chat_session_by_id(session_id: str):
    session = chat_sessions_collection.find_one({"session_id": session_id})
    if session:
        return get_chat_session(session)  # Apply schema for clean data
    return None