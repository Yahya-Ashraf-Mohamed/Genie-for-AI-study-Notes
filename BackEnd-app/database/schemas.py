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
def all_users(users):
    return [inv_data(user) for user in users]


#### Study Materials ####
def Material(study_material):
    return {
        "material_id": study_material["material_id"],
        "title": study_material["title"],
        "content_type": study_material["content_type"],
        "language": study_material["language"]
    }

def all_materials(study_material):
    return[Material(material) for material in study_material]
