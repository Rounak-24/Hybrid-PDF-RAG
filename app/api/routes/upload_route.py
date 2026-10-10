from fastapi import APIRouter, UploadFile, File
from app.api.controllers.upload_controller import upload_file_controller
from app.api.controllers.answer_controller import answer_controller
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    unique_file_id: str

upload_router = APIRouter()

@upload_router.post("/")
async def upload_file(file: UploadFile = File(...)):
    return await upload_file_controller(file)


@upload_router.post("/answer")
async def get_answer(data:QuestionRequest):
    return await answer_controller(data.question, data.unique_file_id)
