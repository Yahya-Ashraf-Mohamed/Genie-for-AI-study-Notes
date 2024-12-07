# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, StudyMaterial
from pinecone_handler import insert_vector_data, query_vector_data  # Import functions from pinecone_handler
from mongodb import insert_generated_content  # Import function to store in MongoDB

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create study material and store its vector data in Pinecone
############# still under development ############
@app.post("/study_material/")
def create_study_material(title: str, content_type: str, db: Session = Depends(get_db)):
    # Insert study material into PostgreSQL
    material = StudyMaterial(title=title, content_type=content_type)
    db.add(material)
    db.commit()
    db.refresh(material)

    # Generate vector embeddings for the material (replace with actual logic)
    embeddings = [0.1, 0.2, 0.3]  # Example, replace this with actual logic

    # Insert the vector into Pinecone
    insert_vector_data(str(material.id), embeddings)

    # Generate content for MongoDB (summary, questions, answers)
    summary = "This is a summary of the material."  # Example summary, replace with actual logic
    questions = ["What is AI?", "Define NLP."]
    answers = ["AI is...", "NLP stands for..."]
    
    # Insert generated content into MongoDB
    insert_generated_content(str(material.id), summary, questions, answers)

    return {"message": f"Study material '{material.title}' added successfully!"}



# create a study material
@app.post("/create/")
async def create_study_material(title: str, content_type: str):
    db = SessionLocal()
    study_material = StudyMaterial(title=title, content_type=content_type)
    db.add(study_material)
    db.commit()
    db.refresh(study_material)
    db.close()
    return {"id": study_material.id, "title": study_material.title, "content_type": study_material.content_type}

# read all study materials
@app.get("/study_materials/")
async def get_study_materials():
    db = SessionLocal()
    study_materials = db.query(StudyMaterial).all()
    db.close()
    return study_materials

# update a study material by ID
@app.put("/study_materials/{id}")
async def update_study_material(id: int, title: str, content_type: str):
    db = SessionLocal()
    study_material = db.query(StudyMaterial).filter(StudyMaterial.id == id).first()
    if not study_material:
        db.close()
        raise HTTPException(status_code=404, detail="Study material not found")
    study_material.title = title
    study_material.content_type = content_type
    db.commit()
    db.refresh(study_material)
    db.close()
    return study_material

# delete a study material by ID
@app.delete("/study_materials/{id}")
async def delete_study_material(id: int):
    db = SessionLocal()
    study_material = db.query(StudyMaterial).filter(StudyMaterial.id == id).first()
    if not study_material:
        db.close()
        raise HTTPException(status_code=404, detail="Study material not found")
    db.delete(study_material)
    db.commit()
    db.close()
    return {"message": "Study material deleted"}

# Error handling for fetching study material by ID
@app.get("/study_material/{id}")
async def get_study_material(id: int):
    db = SessionLocal()
    study_material = db.query(StudyMaterial).filter(StudyMaterial.id == id).first()
    db.close()
    if not study_material:
        raise HTTPException(status_code=404, detail="Study material not found")
    return study_material

# Route to query Pinecone for similar study materials based on a query vector
@app.get("/query_material/")
def query_material(query_vector: list, top_k: int = 5):
    results = query_vector_data(query_vector, top_k)
    return {"results": results}



################### Testing #####################
@app.post("/test_study_material/")
def test_study_material(title : str , content_type : str , db:Session = Depends(get_db)):
    material = StudyMaterial(title=title, content_type=content_type)
    db.add(material)
    db.commit()
    db.refresh(material)
    return {"message": f"Study material '{material.title}' added successfully!"}


@app.get("/study_material/{material_id}")
def get_study_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(StudyMaterial).filter(StudyMaterial.id == material_id).first()
    if material is None:
        return {"error": "Study material not found!"}
    return {"title": material.title, "content_type": material.content_type}
