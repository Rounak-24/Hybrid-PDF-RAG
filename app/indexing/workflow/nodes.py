from app.indexing.workflow.indexing_state import IndexingState
from langchain_community.document_loaders import PyPDFLoader
from app.indexing.text_splitter import split_docs
from app.indexing.graph_transformer import get_llm_graph_transformer
from app.graphstore.neo4j_graph import inset_graph_to_neo4j
from app.vectorstore.qdrant_store import insert_embeddings_to_qdrant
from langsmith import traceable


@traceable(name="pdf_loader_fn")
async def load_pdf(state:IndexingState):
    try:
        from pathlib import Path
        local_file_path = state["local_filepath"]

        if (local_file_path==None or Path(local_file_path).exists()==False):
            raise Exception("File path is missing")
        
        loader = PyPDFLoader(local_file_path)
        docs = await loader.aload()
        state["file_docs"] = docs

        print("PDF loaded to docs successfully....")
        return state


    except Exception as e:
        print("Something went wrong while loading PDF")
        raise e


@traceable(name="chunk_file_fn")
async def chunk_file(state:IndexingState):
    docs = state["file_docs"]
    if docs==None or len(docs)==0:
        raise Exception("file_docs are mising....")

    chunks = await split_docs(docs)
    unique_file_id = state["unique_file_id"]

    import uuid

    for chunk in chunks:
        chunk.metadata["file_id"] = unique_file_id
        chunk.metadata['id'] = str(uuid.uuid4())
    # print(chunks)
    return { 'chunks':chunks }


@traceable(name="chunks_to_graph_docs_fn")
async def chunks_to_graph_docs(state:IndexingState):
    chunks = state["chunks"]
    if chunks==None or len(chunks)==0:
        raise Exception("chunks are mising inside chunks_to_graph_docs node....")

    graph_transformer = get_llm_graph_transformer()
    graph_docs = await graph_transformer.aconvert_to_graph_documents(documents=chunks)
    # print(graph_docs)
    return { 'graph_docs': graph_docs }


@traceable(name="insert_knowledge_graph_fn")
async def insert_knowledge_graph(state:IndexingState):
    graph_docs = state["graph_docs"]
    if graph_docs==None or len(graph_docs)==0:
        raise Exception("graph_docs are mising....")

    await inset_graph_to_neo4j(graph_docs)
    return {}


@traceable(name="store_vector_embeddings_fn")
async def store_vector_embeddings(state:IndexingState):
    chunks = state["chunks"]
    if chunks==None or len(chunks)==0:
        raise Exception("chunks are mising inside store_vector_embeddings node....")

    ids = await insert_embeddings_to_qdrant(chunks)
    return {}


@traceable(name="indexing_completed_fn")
async def indexing_completed(state:IndexingState):
    state["success"] = True
    local_file_path = state["local_filepath"]
    print(f"Indexing of file:{local_file_path} has been completed....")

    return state