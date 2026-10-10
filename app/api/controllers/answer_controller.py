from fastapi import HTTPException


async def answer_controller(question:str, unique_file_id:str):
    try:
        if question==None or question=="" or unique_file_id==None:
            raise HTTPException(status_code=400, detail="question or unique_file_id is missing in the answer_controller....")

        from app.retrieving.workflow.graph import retrieve_answer
        answer = await retrieve_answer(unique_file_id, question)  
        
        if answer==None or len(answer)==0:
            raise HTTPException(status_code=500, detail="answer is empty in the answer_controller....")

        return { 'answer':answer, 'success':True, 'status':200 }

    except Exception as e:
        if isinstance(e, HTTPException): raise e
        else: raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")