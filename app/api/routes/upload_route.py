from fastapi import APIRouter, UploadFile, File
from app.api.controllers.upload_controller import upload_file_controller
from app.api.controllers.index_controller import index_file_controller
from pydantic import BaseModel

class IndexRequest(BaseModel):
    unique_file_id:str
    filename_in_server:str

upload_router = APIRouter()

@upload_router.post("/")
async def upload_file(file: UploadFile = File(...)):
    return await upload_file_controller(file)


@upload_router.post("/index")
async def get_answer(data:IndexRequest):
    return await index_file_controller(
        unique_file_id = data.unique_file_id,
        local_file_path = data.filename_in_server
    )