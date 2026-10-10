from app.retrieving.workflow.retrieving_state import RetrievalState
from app.vectorstore.qdrant_store import search_vector_store
from app.graphstore.neo4j_graph import search_neo4j_graph
from app.retrieving.answer_generator import generate_answer
from langsmith import traceable


@traceable(name="vector_search_fn")
async def search_in_vector_db(state:RetrievalState):
    question = state['question']
    unique_file_id = state['unique_file_id']

    if question==None or unique_file_id==None:
        raise Exception("user question or file_id is missing in the vector_search_node....")

    result_chunk_ids, result_chunk_content = await search_vector_store(question,unique_file_id)

    return {
        'vector_search_chunk_ids':result_chunk_ids,
        'vector_search_result':result_chunk_content
    }


@traceable(name='graph_search_fn')
async def search_in_graph_db(state:RetrievalState):
    vector_search_chunk_ids = state['vector_search_chunk_ids']
    if vector_search_chunk_ids==None or len(vector_search_chunk_ids)==0:
        raise Exception("vector_search_chunk_ids are missing in the graph_search_node....") 

    graph_search_result = await search_neo4j_graph(vector_search_chunk_ids)
    return { 'graph_search_result':graph_search_result }


@traceable(name='generate_answer_fn')
async def answer_generation(state:RetrievalState):
    question = state['question']
    vector_search_result = state['vector_search_result']
    graph_search_result = state['graph_search_result']

    if question==None or vector_search_result==None or graph_search_result==None:
        raise Exception("question or vector_search_result or graph_search_result is missing in the generate_answer_node....")

    answer = await generate_answer(question, vector_search_result, graph_search_result)

    if answer==None or len(answer)==0:
        raise Exception("answer is empty in the generate_answer_node....")
    
    return { 'answer':answer, 'success':True }