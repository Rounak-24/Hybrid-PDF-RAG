from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

openai = None

def get_openai_llm():
    global openai

    if openai==None:
        openai = ChatOpenAI(
            api_key = os.getenv('OPENAI_API_KEY'),
            model = 'gpt-4o-mini-2024-07-18'
        )

    return openai