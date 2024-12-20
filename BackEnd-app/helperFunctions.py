from datetime import datetime
from database.schemas import get_chat_session
from config import *
from AI import *
from main import rag_instances

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


def get_rag_response(session_id: str, material_path: str, message: str, chat_history: list):
    """
    Retrieves a response from the RAG model while ensuring
    that only one instance of the RAG model is active per session.
    """
    # Check if the RAG model instance exists
    if session_id not in rag_instances:
        # Create and load memory for a new instance
        rag_model = RagChain(source_name=material_path)
        rag_model.load_memory(chat_history)
        rag_instances[session_id] = rag_model
    else:
        # Use existing instance
        rag_model = rag_instances[session_id]

    # Ask the question and return the response
    response = rag_model.ask_question(message)
    return response