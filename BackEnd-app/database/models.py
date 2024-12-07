from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    isPremium: bool


class StudyMaterial(BaseModel):
    material_id : str
    title : str
    content_type : str
    language : str


class Summary(BaseModel):
    Summary_id : str
    material_id : str
    content : str
    detail_level : str

class FlashCard(BaseModel):
    flash_id : str
    

