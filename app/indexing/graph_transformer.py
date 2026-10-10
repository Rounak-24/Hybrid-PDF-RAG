from langchain_neo4j import LLMGraphTransformer
from app.llm.openai_llm import get_openai_llm

openai = get_openai_llm()
llm_transformer = None

def get_llm_graph_transformer():
    global llm_transformer

    if llm_transformer==None:
        llm_transformer = LLMGraphTransformer(llm=openai)
        
    return llm_transformer
