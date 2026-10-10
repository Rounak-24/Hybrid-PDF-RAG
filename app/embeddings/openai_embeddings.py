from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
import os

embedder = None

def get_embedder():
    global embedder

    if embedder==None:
        embedder = OpenAIEmbeddings(
            api_key=os.getenv('OPENAI_API_KEY'),
            model='text-embedding-3-large'
        )

    return embedder