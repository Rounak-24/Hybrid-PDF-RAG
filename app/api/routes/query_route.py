from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.api.controllers.answer_controller import answer_controller
from pydantic import BaseModel
import asyncio

class QuestionRequest(BaseModel):
    question: str
    unique_file_id: str

query_router = APIRouter()

async def stream_string_generator(full_text: str):
    words = full_text.split(" ")
    for word in words:
        yield f"{word} "
        await asyncio.sleep(0.02)

@query_router.post('/', response_class = StreamingResponse)
async def query_file_route(data:QuestionRequest):
    answer = await answer_controller(data.question, data.unique_file_id)

    return StreamingResponse(
        stream_string_generator(answer), 
        media_type = "text/plain",
        status_code = 200
    )