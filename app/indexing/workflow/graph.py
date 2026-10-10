from langgraph.graph import StateGraph, END, START
from app.indexing.workflow.indexing_state import IndexingState

from app.indexing.workflow.nodes import (
    load_pdf, 
    chunk_file, 
    chunks_to_graph_docs, 
    insert_knowledge_graph, 
    store_vector_embeddings, 
    indexing_completed
)


graph_builder = StateGraph(IndexingState)

graph_builder.add_node('load_pdf', load_pdf)
graph_builder.add_node('chunk_file', chunk_file)
graph_builder.add_node('chunks_to_graph_docs', chunks_to_graph_docs)
graph_builder.add_node('insert_knowledge_graph', insert_knowledge_graph)
graph_builder.add_node('store_vector_embeddings', store_vector_embeddings)
graph_builder.add_node('indexing_completed', indexing_completed)


graph_builder.add_edge(START, 'load_pdf')
graph_builder.add_edge('load_pdf', 'chunk_file')

graph_builder.add_edge('chunk_file', 'chunks_to_graph_docs')
graph_builder.add_edge('chunk_file', 'store_vector_embeddings')

graph_builder.add_edge('chunks_to_graph_docs', 'insert_knowledge_graph')

graph_builder.add_edge(
    ['store_vector_embeddings', 'insert_knowledge_graph'],
    'indexing_completed'
)

graph_builder.add_edge('indexing_completed', END)


indexing_workflow = graph_builder.compile()


async def index_file(local_filepath:str, unique_file_id:str):
    try:
        initial_state = IndexingState(
            local_filepath=local_filepath,
            unique_file_id=unique_file_id
        )

        final_state = await indexing_workflow.ainvoke(initial_state)
        
        if final_state.get('success')==True: return True
        else: return False

    except Exception as e:
        print("something went wrong while indexing....", e)
        return False