from fastapi import FastAPI, APIRouter, HTTPException
from config import *
from database.schemas import *
from database.models import *
app = FastAPI()
router = APIRouter()

# @router.get("/")
# async def read_root():
#     return {"message": "Welcome to the FastAPI backend!"}



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





# @router.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     x = ["xxxx","yyyyyy"]
#     q = x[item_id]
#     return {"item_id": item_id, "q": q}


app.include_router(router)