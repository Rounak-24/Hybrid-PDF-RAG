from langgraph.graph import StateGraph, START, END
from app.retrieving.workflow.retrieving_state import RetrievalState
from app.retrieving.workflow.nodes import search_in_vector_db, search_in_graph_db, answer_generation 


graph_builder = StateGraph(RetrievalState)

graph_builder.add_node('search_in_vector_db', search_in_vector_db)
graph_builder.add_node('search_in_graph_db', search_in_graph_db)    
graph_builder.add_node('answer_generation', answer_generation)

graph_builder.add_edge(START, 'search_in_vector_db')
graph_builder.add_edge('search_in_vector_db', 'search_in_graph_db')
graph_builder.add_edge('search_in_graph_db', 'answer_generation')
graph_builder.add_edge('answer_generation', END)


retrieval_workflow = graph_builder.compile()


async def retrieve_answer(unique_file_id:str, question:str):
    try:
        initial_state = RetrievalState(
            unique_file_id=unique_file_id,
            question=question
        )

        final_state = await retrieval_workflow.ainvoke(initial_state)
        return final_state.get('answer')

    except Exception as e:
        print("something went wrong while retrieving answer....", e)
        raise e