from typing import TypedDict, Any


class RetrievalState(TypedDict):
    unique_file_id: str
    question: str

    vector_search_result: list[dict[str,Any]]
    vector_search_chunk_ids: list[str]
    graph_search_result: list[str]

    answer: str
    success: bool