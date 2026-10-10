from typing import TypedDict
from langchain_core.documents import Document
from langchain_neo4j.graphs.graph_document import GraphDocument


class IndexingState(TypedDict):
    local_filepath:str
    unique_file_id:str

    file_docs: list[Document]
    chunks: list[Document]
    graph_docs: list[GraphDocument]

    success: bool