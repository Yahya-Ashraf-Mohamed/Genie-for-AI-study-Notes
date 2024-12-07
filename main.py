from fastapi import FastAPI, HTTPException
from mongodb import insert_generated_content, mongo_db

app = FastAPI()

# Reference to the MongoDB collection
study_materials = mongo_db["study_materials"]

# Route to create study material and store it in MongoDB
@app.post("/create/")
async def create_study_material(title: str, content_type: str):
    study_material = {
        "title": title,
        "content_type": content_type
    }
    result = study_materials.insert_one(study_material)
    return {"id": str(result.inserted_id), "title": title, "content_type": content_type}


# Read all study materials
@app.get("/study_materials/")
async def get_study_materials():
    materials = list(study_materials.find({}, {"_id": 0}))
    return materials


# Fetch a specific study material by ID
@app.get("/study_material/{material_id}")
async def get_study_material(material_id: str):
    material = study_materials.find_one({"_id": material_id}, {"_id": 0})
    if not material:
        raise HTTPException(status_code=404, detail="Study material not found")
    return material


# Route to test inserting generated content
@app.post("/test_generated_content/")
async def test_generated_content(material_id: str, summary: str, questions: list, answers: list):
    insert_generated_content(material_id, summary, questions, answers)
    return {"message": "Generated content inserted successfully"}
