from langchain_neo4j import Neo4jGraph
from langchain_neo4j.graphs.graph_document import GraphDocument
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


neo4j_graph = Neo4jGraph(
    url = os.getenv("NEO4J_URI"),
    username = os.getenv("NEO4J_USERNAME"),
    password = os.getenv("NEO4J_PASSWORD"),
    database = os.getenv("NEO4J_DATABASE"),
    refresh_schema=False,
    driver_config={
        "connection_timeout": 30,
        "max_connection_lifetime": 300,
        "max_transaction_retry_time": 60,
        "keep_alive": True,
    }
)


async def inset_graph_to_neo4j(graph_docs:list[GraphDocument]):
    try:

        await asyncio.to_thread(
            neo4j_graph.add_graph_documents,
            graph_docs,
            include_source=True
        )

        print("Graph inserted to Neo4j Store....")

    except Exception as e:
        print("Something went wrong while inserting graph to neo4j")
        raise e



async def search_neo4j_graph(chunk_ids:list[str]):
    try:
        cypher_query = """
            MATCH (c:Document)-[:MENTIONS]->(e)
            WHERE c.id IN $chunk_ids
            WITH collect(DISTINCT e) AS seeds
            UNWIND seeds AS s
            MATCH (s)-[r]-(n)
            WHERE type(r) <> 'MENTIONS'
            AND NOT n:Document
            AND NOT s:Document
            WITH DISTINCT r
            RETURN startNode(r).id + ' -[' + type(r) + ']-> ' + endNode(r).id AS triple
            LIMIT 100
        """

        query_params = { 'chunk_ids':chunk_ids }

        results = await asyncio.to_thread(
            neo4j_graph.query,
            cypher_query,
            params=query_params
        )

        print(results)
        relationships:list[str] = []

        for result in results:
            relation = result['triple']
            relationships.append(relation)

        return relationships

    except Exception as e:
        print("Something went wrong while searching graph in neo4j")
        raise e