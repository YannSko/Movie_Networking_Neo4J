import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from neo4j import GraphDatabase

# Connect to the Neo4j database
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def get_graph_data():
    query = '''
    MATCH (u:User)-[r:RATED]->(m:Movie)
    RETURN u.id AS userId, m.title AS movieTitle, r.rating AS rating LIMIT 50
    '''
    with driver.session() as session:
        result = session.run(query)
        nodes = set()
        edges = []
        for record in result:
            user_node = Node(id=f"User_{record['userId']}", label=f"User {record['userId']}", size=300)
            movie_node = Node(id=f"Movie_{record['movieTitle']}", label=record['movieTitle'], size=400)
            nodes.add(user_node)
            nodes.add(movie_node)
            edges.append(Edge(source=user_node.id, target=movie_node.id, label=f"Rated: {record['rating']}"))
        return list(nodes), edges

nodes, edges = get_graph_data()

# Graph configuration
config = Config(width=800, height=600, directed=True)

# Render the graph in Streamlit
agraph(nodes=nodes, edges=edges, config=config)
