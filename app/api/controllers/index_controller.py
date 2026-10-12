from fastapi import HTTPException
from app.indexing.workflow.graph import index_file
from pathlib import Path
import os


async def index_file_controller(unique_file_id:str, local_file_path:str):
    try:
        if unique_file_id==None or local_file_path==None:
            raise HTTPException(400,'unique_file_id or filename_in_serser is missing')

        indexing_done = await index_file(local_file_path, unique_file_id)
        if Path(local_file_path).exists(): os.remove(local_file_path)

        if indexing_done:
            return {
                "success":True,
                "status":200,
                "message":"File has been indexed successfully",
                "filename_in_server": local_file_path,
                "unique_file_id":unique_file_id,
                "indexing": True
            }

        else: raise Exception('Something went wrong while indexing')

    except Exception as e:
        if isinstance(e, HTTPException): raise e
        else: raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")