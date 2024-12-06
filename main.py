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

# Route to query Pinecone for similar study materials based on a query vector
@app.get("/query_material/")
def query_material(query_vector: list, top_k: int = 5):
    results = query_vector_data(query_vector, top_k)
    return {"results": results}
