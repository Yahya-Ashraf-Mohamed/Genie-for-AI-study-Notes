from fastapi import FastAPI, APIRouter, HTTPException
from config import *
from bson.objectid import ObjectId
from database.schemas import *
from database.models import *
app = FastAPI()
router = APIRouter()
from helperFunctions import *


@router.get("/")
async def hello():
    return {"status code": 200,"message":"hello to our website"}


###############     User        ##############

@router.get("/users/", tags=["Users"])
async def read_all_users():
    data = user_collection.find()
    return get_all_users(data)


@app.get("/user/{user_id}", tags=["Users"])
async def read_user(user_id: str):
    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return mongo_to_dict(user)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/user/", tags=["Users"])
async def create_user(user:User):
    try:
        res = user_collection.insert_one(dict(user))
        return {"status code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")

###############     Quiz        ##############

@router.get("/quizzes/", tags=["Quizzes"])
async def read_all_quizzes():
    data = quiz_collection.find()
    return get_all_quizzes(data)

#### Study Material ####
@router.post("/study_materials/", tags=["Study Materials"])
async def add_study_material(material: StudyMaterial):
    try:
        # Insert material into MongoDB
        resp = study_material_collection.insert_one(material.dict())
        return {"status_code": 200, "id": str(90)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting study material: {e}")
    

@router.get("/study_materials/", tags=["Study Materials"])
async def view_study_materials(material:StudyMaterial):
    try:
        data = study_material_collection.find()
        return all_materials(data)
    except Exception as e :
        print("no study material")


@app.get("/search/", tags=["Study Materials"])
async def search_study_material(title: str):
    try:
       
        results = study_material_collection.find({"title": {"$regex": title, "$options": "i"}})
        materials = [StudyMaterial(**result) for result in results]
        if not materials:
            raise HTTPException(status_code=404, detail="No study materials found with that title.")
        
        return {"status_code": 200, "found_materials": materials}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for study materials: {e}")

@app.get("/quiz/{quiz_id}", tags=["Quizzes"])
async def read_quiz(quiz_id: str):
    try:
        quiz = quiz_collection.find_one({"_id": ObjectId(quiz_id)})
        if quiz:
            return mongo_to_dict(quiz)
        else:
            raise HTTPException(status_code=404, detail="quiz not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quiz/", tags=["Quizzes"])
async def create_quiz(quiz:Quiz):
    try:
        res = quiz_collection.insert_one(dict(quiz))
        return {"status code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


app.include_router(router)