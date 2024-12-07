from fastapi import FastAPI, APIRouter
from config import collection
from database.schemas import inv_data, all_users
from database.models import User
app = FastAPI()
router = APIRouter()

# @router.get("/")
# async def read_root():
#     return {"message": "Welcome to the FastAPI backend!"}


@router.get("/")
async def Read_users():
    data = collection.find()
    return all_users(data)


@router.post("/")
async def create_user(user:User):
    try:
        resp = collection.insert_one(dict(user))
        return {"status code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")



# @router.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     x = ["xxxx","yyyyyy"]
#     q = x[item_id]
#     return {"item_id": item_id, "q": q}


app.include_router(router)