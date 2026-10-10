from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from qdrant_client import QdrantClient, models
from typing import Any
from app.embeddings.openai_embeddings import get_embedder
import os
from dotenv import load_dotenv
load_dotenv()

openai_embedder = get_embedder()

_qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# _qdrant_client = QdrantClient(url='http://localhost:6333')

vector_store = QdrantVectorStore(
    client = _qdrant_client,
    collection_name = os.getenv("QDRANT_COLLECTION"),
    embedding = openai_embedder
)

vector_store.client.create_payload_index(
    collection_name = os.getenv("QDRANT_COLLECTION"),
    field_name = "metadata.file_id",
    field_schema = models.PayloadSchemaType.KEYWORD,
)

async def insert_embeddings_to_qdrant(docs:list[Document]):
    try:
        chunk_ids = await vector_store.aadd_documents(docs)
        print('Docs added to vector store....')
        return chunk_ids
        
    except Exception as e:
        print("Something went wrong while storing vector embeddings....")
        raise e



async def search_vector_store(question:str, unique_file_id:str):
    try:
        result_docs = await vector_store.asimilarity_search(
            query = question,
            k = 4,
            filter = models.Filter(
                must = models.FieldCondition(
                    key ='metadata.file_id',
                    match = models.MatchValue(value=unique_file_id)
                )
            )
        )

        result_chunk_ids:list[str] = []
        result_chunk_content:list[dict[str,Any]] = []

        for doc in result_docs:
            chunk_id = doc.metadata.get('id')

            page_dict = {
                'page_content': doc.page_content,
                'page_label':doc.metadata.get('page_label'),
                'page':doc.metadata.get('page')
            }

            result_chunk_ids.append(chunk_id)
            result_chunk_content.append(page_dict)

        return result_chunk_ids, result_chunk_content 

    except Exception as e:
        print("Something went wrong in vector_search....")
        raise e