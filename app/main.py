from fastapi import FastAPI
import uvicorn
from app.api.routes.upload_route import upload_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(upload_router,prefix="/upload")

@app.get("/health")
async def health_handler():
    return {
        "status":"ok",
        "success":True,
        "message":"Server is up & running...."
    }

def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )

if __name__=="__main__":
    main()