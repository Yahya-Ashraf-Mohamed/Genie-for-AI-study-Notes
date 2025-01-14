from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import *
# from bson.objectid import ObjectId
from database.schemas import *
from database.models import *
from fastapi import Request
from fastapi import File, UploadFile
import shutil
from pathlib import Path
from fastapi.responses import JSONResponse
from AI.pdf_pipeline import *
from AI.qa_pipeline import *
from helperFunctions import *

# Access the keys from the environment
os.environ["PINECONE_API_KEY"] = "pcsk_7a6x6_Mq2MQntZVjiiXLLpdPWXfKdgKatSLRn3FHrETqvixgyR6TEJoZBbw7CtBYAaWnk" 
os.environ["GROQ_API_KEY"] = "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"

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
    return "ok"#await create_chat()


###############     User        ##############

@router.get("/users/", tags=["Users"])
async def read_all_users():
    data = user_collection.find()
    return get_all_users(data)


# @app.get("/user/{user_id}", tags=["Users"])
# async def read_user(user_id: str):
#     try:
#         user = user_collection.find_one({"_id": ObjectId(user_id)})
#         if user:
#             return mongo_to_dict(user)
#         else:
#             raise HTTPException(status_code=404, detail="User not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

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

# @router.get("/study_material/{material_id}", tags=["Study Materials"])
# async def view_study_material(material_id: str):
#     try:
#         material = study_material_collection.find_one({"_id": ObjectId(material_id)})
#         if material:
#             return mongo_to_dict(material)
#         else:
#             raise HTTPException(status_code=404, detail="material not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


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




###############      Chat conversation: Q&A       ##############

####################fatma ######################3
material=None
qa_rag_instance=None
@router.post("/newchat", tags=["chats"])
async def create_chat(material_path: str):
    global material
    material=material_path
    try:
        return {"message": f"Model instance for '{material_path}' is successfully prepared."}

    except Exception as e:
        # Catch and return any errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/ask_rag_model", tags=["chats"])
async def ask_question(question: str):
    global material, qa_rag_instance
    print("material", material)
    if qa_rag_instance is None:
        qa_rag_instance = RagChain(source_name=material)
    try:
        print(qa_rag_instance.source_name)  # Corrected 'souce_name' to 'source_name'
        model_answer = qa_rag_instance.ask_question(question)  # Ask the question and get the response
        return {"answer": model_answer}
    except Exception as e:
        # Catch and return any errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



###############################################3

# @app.get("/chat/{file_path}", tags=["chats"])
# async def read_chat(file_path: str):
#     try:
#         chat = chat_sessions_collection.find_one({"file_path": file_path})
#         if chat:
#             return mongo_to_dict(chat)
#         else:
#             response = await create_chat(file_path)
#             return response
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("/newchat", tags=["chats"])
# async def create_chat(material_path: str):
#     try:
#         new_chat = {
#             "material_path": material_path,
#             "chat_history": [],
#             "created_at": datetime.now(),
#             "last_active_at": datetime.now()
#         }
#         result = chat_sessions_collection.insert_one(new_chat)

#         # Initialize the RAG model and store it in the dictionary
#         rag_model = RagChain(source_name=material_path)
#         rag_model.perform_embedding()
#         rag_instances[ObjectId] = rag_model

#         return {"status": "success", "chat_id": ObjectId}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating chat session: {e}")

# @router.post("/SendMessage", tags=["chats"])
# async def send_message(message: IncomingChatMessage):
#     """
#     Handles user messages, queries the RAG model, and updates chat history.
#     """
#     try:
#         # Fetch the chat session
#         chat = chat_sessions_collection.find_one({"_id": ObjectId(message.chat_session_id)})
#         if not chat:
#             raise HTTPException(status_code=404, detail="Chat session not found")

#         # Append user's message to the chat history
#         user_message = ChatMessage(sender="user", message=message.message_content, timestamp=datetime.now())
#         chat["chat_history"].append(user_message.dict())

#         # Generate the RAG model's response
#         answer = get_rag_response(
#             session_id=message.chat_session_id,
#             material_path=chat["material_path"],
#             message=message.message_content,
#             chat_history=chat["chat_history"]
#         )

#         # Append the model's response to the chat history
#         system_message = ChatMessage(sender="system", message=answer, timestamp=datetime.now())
#         chat["chat_history"].append(system_message.dict())

#         # Update the chat history in the database
#         chat_sessions_collection.update_one(
#             {"_id": ObjectId(message.chat_session_id)},
#             {
#                 "$set": {
#                     "chat_history": chat["chat_history"],
#                     "last_active_at": datetime.now()
#                 }
#             }
#         )

#         return {"status": "success", "response": answer, "chat_history": chat["chat_history"]}

#         """""
#         # Create a new ChatMessage instance
#         new_message = ChatMessage(sender=True, message=answer)
#         updated_chat_history = chat.get("chat_history", [])
#         updated_chat_history.append(new_message.dict())
#         # Update the chat session in the database
#         chat_sessions_collection.update_one(
#             {"_id": ObjectId(message.chat_session_id)},
#             {"$set": {"chat_history": updated_chat_history}}
#         )
#         return {"status code": 200, "message": "Message added successfully"}
#         """""
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error in send_message: {e}")


@router.post("/resume_chat")
async def resume_chat(session_id: str, question: str):
    try:
        # Retrieve the chat session from the database
        chat_session = chat_sessions_collection.find_one({"session_id": session_id})
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Ask a question and get the response
        answer = get_rag_response(
            session_id=session_id,
            material_path=chat_session["material_path"],
            message=question,
            chat_history=chat_session["chat_history"]
        )

        # Add the new user and system messages to chat history
        new_user_message = {"sender": "user", "message": question, "timestamp": datetime.now()}
        system_message = {"sender": "system", "message": answer, "timestamp": datetime.now()}

        # Update chat history in the database
        updated_chat_history = chat_session["chat_history"]
        updated_chat_history.extend([new_user_message, system_message])

        chat_sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"chat_history": updated_chat_history}}
        )

        return {"response": answer, "chat_history": updated_chat_history}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resuming chat: {e}")




###############     Quiz        ##############

@router.post("/createquiz/", tags=["Quizzes"])
async def create_quiz(quiz:Quiz):
    try:
        res = quiz_collection.insert_one(dict(quiz))
        return {"status code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.post("/validatequizanswers/", tags=["Quizzes"])
async def validate_quiz_answers(quiz:Quiz):
    pass


# @router.get("/quizzes/", tags=["Quizzes"])
# async def read_all_quizzes():
#     data = quiz_collection.find()
#     return get_all_quizzes(data)


# @app.get("/quiz/{quiz_id}", tags=["Quizzes"])
# async def read_quiz(quiz_id: str):
#     try:
#         quiz = quiz_collection.find_one({"_id": ObjectId(quiz_id)})
#         if quiz:
#             return mongo_to_dict(quiz)
#         else:
#             raise HTTPException(status_code=404, detail="quiz not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.get("/search_quizzes/", tags=["Quizzes"]) ##to be edited
# async def search_study_material(title: str):
#     try:
       
#         results = study_material_collection.find({"title": {"$regex": title, "$options": "i"}})
#         materials = [StudyMaterial(**result) for result in results]
#         if not materials:
#             raise HTTPException(status_code=404, detail="No study materials found with that title.")
        
#         return {"status_code": 200, "found_materials": materials}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error searching for quizzes: {e}")



###############     Exception Handling       ##############



@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"status code": 404, "message": "Hey, endpoint not found. Please check the URL."},
    )

UPLOAD_DIR = Path("../Storage")
UPLOAD_DIR.mkdir(exist_ok=True)  

# Create upload directory if not exists
@app.post("/uploadfile/", tags=["files"])
async def upload_file(file: UploadFile):
    file_location = UPLOAD_DIR / file.filename
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    try:
        # create embedding for the pdf file in Pinecone
        pipeline = PDFPipeline(file_location)
        asyncio.run(pipeline.run())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not create embedding for the uploaded pdf {str(e)}")


    return {"info": f"File '{file.filename}' saved at '{file_location}'"}


@app.get("/home/", tags=["files"])
async def list_files():
    try:
        # Get all files in the directory
        files = [file.name for file in UPLOAD_DIR.iterdir() if file.is_file()]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading files: {str(e)}")


app.include_router(router)


