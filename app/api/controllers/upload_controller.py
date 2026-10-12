from fastapi import UploadFile, HTTPException, File
from pathlib import Path
import uuid
import shutil


def save_file(file:UploadFile):
    filename = file.filename
    unique_id = uuid.uuid4()
    temp_directory = "./public/uploads"
    unique_filename = f"{unique_id}-{filename}"

    try:
        temp_path = Path(f"{temp_directory}/{unique_filename}")
        
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("File has been saved....")
        return f'{temp_directory}/{unique_filename}', unique_id

    except Exception as e:
        print(f"Error for saving file:{filename}, Error:{e}")
        raise e

    finally: file.file.close()


async def upload_file_controller(file:UploadFile = File(...)):
    try:
        if file==None:
            raise HTTPException(400,"File is missing....")

        filename = file.filename
        if(not filename.endswith(".pdf")):
            raise HTTPException(400,"invalid file type")
        
        local_file_path, unique_file_id = save_file(file)
        
        return {
            "success":True,
            "status":200,
            "message":"File has been uploaded successfully",
            "filename_in_server": local_file_path,
            "unique_file_id":unique_file_id,
            "indexing": False
        }

    except Exception as e:
        if isinstance(e, HTTPException): raise e
        else: raise HTTPException(500,f"Internal Server Error: {e}")