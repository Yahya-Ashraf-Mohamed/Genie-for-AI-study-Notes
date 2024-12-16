from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import *
from bson.objectid import ObjectId
from database.schemas import *
from database.models import *
from fastapi import Request
from fastapi.responses import JSONResponse
from AI import PDFProcessor
from helperFunctions import *




app = FastAPI(title="Genie - AI Study Assistant")

origins = ['http://localhost:3000']  #
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

router = APIRouter()
from helperFunctions import *


@router.get("/")
async def hello():
    return await create_chat()


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

@router.post("/user", tags=["Users"]) 
async def create_user(user: User):
    try:
        res = user_collection.insert_one(dict(user))
        return {"status code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@app.get("/search_users/", tags=["Users"]) ##to be edited

async def search_study_material(title: str):
    try:
       
        results = study_material_collection.find({"title": {"$regex": title, "$options": "i"}})
        materials = [StudyMaterial(**result) for result in results]
        if not materials:
            raise HTTPException(status_code=404, detail="No study materials found with that title.")
        
        return {"status_code": 200, "found_materials": materials}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for users: {e}")



###############     Quiz        ##############

@router.get("/quizzes/", tags=["Quizzes"])
async def read_all_quizzes():
    data = quiz_collection.find()
    return get_all_quizzes(data)


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

@app.get("/search_quizzes/", tags=["Quizzes"]) ##to be edited
async def search_study_material(title: str):
    try:
       
        results = study_material_collection.find({"title": {"$regex": title, "$options": "i"}})
        materials = [StudyMaterial(**result) for result in results]
        if not materials:
            raise HTTPException(status_code=404, detail="No study materials found with that title.")
        
        return {"status_code": 200, "found_materials": materials}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for quizzes: {e}")



###############     Study material       ##############

@router.post("/study_materials/", tags=["Study Materials"])
async def add_study_material(material: StudyMaterial):
    try:
        # Insert material into MongoDB
        res = study_material_collection.insert_one(material.dict())
        return {"status_code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting study material: {e}")
    

@router.get("/study_materials/", tags=["Study Materials"])
async def view_study_materials():
    try:
        data = study_material_collection.find()
        return all_materials(data)
    except Exception as e :
        print("no study material")

@router.get("/study_material/{material_id}", tags=["Study Materials"])
async def view_study_material():
    try:
        material = study_material_collection.find_one({"_id": ObjectId(material_id)})
        if material:
            return mongo_to_dict(material)
        else:
            raise HTTPException(status_code=404, detail="material not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/search_study_materials/", tags=["Study Materials"])
async def search_study_material(title: str):
    try:
       
        results = study_material_collection.find({"title": {"$regex": title, "$options": "i"}})
        materials = [StudyMaterial(**result) for result in results]
        if not materials:
            raise HTTPException(status_code=404, detail="No study materials found with that title.")
        
        return {"status_code": 200, "found_materials": materials}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for study materials: {e}")




###############     Create Chat       ##############

# @router.get("/chats/", tags=["chats"])
# async def read_all_users():
#     data = user_collection.find()
#     return get_all_users(data)


















###############     Exception Handling       ##############



@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"status code": 404, "message": "Hey, endpoint not found. Please check the URL."},
    )





app.include_router(router)


