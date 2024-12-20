from database.models import *

###############     User        ##############
def get_user(user: dict):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"],
        "isPremium": user["isPremium"],
        "email": user["email"],
        "registrationDate": user["registrationDate"],
        "preferences": user["preferences"],
        "studyGoals": user["studyGoals"],
        "usageStats": user["usageStats"],
        "progressReports": user["progressReports"]
    }

def get_all_users(users):
    return [get_user(user) for user in users]


###############     Quiz        ##############

def get_quiz(quiz: Quiz):
    return {
        "title": quiz["title"],
        "description": quiz["description"],
        "creator": quiz["creator"],
        "creationDate": quiz["creationDate"],
        "dueDate": quiz["dueDate"],
        "questions": quiz["questions"],
        "isPublic": quiz["isPublic"],
        "category": quiz["category"],
        "maxAttempts": quiz["maxAttempts"],
        "passingScore": quiz["passingScore"],
        "feedback": quiz["feedback"],
    }

def get_all_quizzes(quizzes):
    return [get_user(quiz) for quiz in quizzes]



#### Study Materials ####
def Material(study_material):
    return {
        "material_id": study_material["material_id"],
        "title": study_material["title"],
        "description": study_material.get("description", None),
        "content_type": study_material["content_type"],
        "language": study_material["language"],
        "file_url": study_material["file_url"],
        "uploaded_date": study_material["uploaded_date"],
        "category": study_material.get("category", None),
        "is_public": study_material.get("is_public", True)
    }

def all_materials(study_material):
    return[Material(material) for material in study_material]



##########      Summary     ##########
def get_summary_result(summary):
    return {
        "summary_id": summary["summary_id"],
        "material_id": summary["material_id"],
        "generated_summary": summary["generated_summary"],
        "detail_level": summary["detail_level"],
    }

def get_all_summaries(summaries):
    return [get_summary_result(summary) for summary in summaries]



##########      chat        ############

def get_chat_message(message: dict):
    """
    Converts a single chat message document to a Python dictionary.
    """
    return {
        "sender": message["sender"],  # 'user' or 'system'
        "message": message["message"],
        "timestamp": message["timestamp"],
    }


def get_chat_session(session: dict):
    """
    Converts a chat session document to a Python dictionary.
    """
    return {
        "session_id": session["session_id"],
        "material_id": session["material_id"],
        "chat_history": [get_chat_message(msg) for msg in session.get("chat_history", [])],
    }