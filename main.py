from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, StudyMaterial

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a new study material
@app.post("/study_material/")
def create_study_material(title: str, content_type: str, db: Session = Depends(get_db)):
    material = StudyMaterial(title=title, content_type=content_type)
    db.add(material)
    db.commit()
    db.refresh(material)
    return {"message": f"Study material '{material.title}' added successfully!"}
