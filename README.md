# Movie_Recommander

 Dataset from : https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset/data

Movie Recommender System

This project is a Movie Recommendation System built using Neo4j for graph database functionality and Streamlit for an interactive front-end. The system ingests a dataset consisting of movie ratings, tags, and metadata to create a dynamic recommendation engine based on user preferences, tags, and movie ratings.
Objective

The goal of this project is to:

    Explore relationships between users, movies, tags, and ratings using a graph-based database (Neo4j).
    Provide movie recommendations based on user ratings and preferences.
    Visualize the graph relationships interactively through Streamlit, allowing users to explore movies, tags, and related users dynamically.

Technology Stack

    Neo4j: A graph database used to store and query relationships between movies, users, tags, and ratings.
    Streamlit: A Python framework for building interactive web applications.
    Python: For data processing and interacting with Neo4j.

Dataset Overview

The dataset includes the following files:

    movies.csv: Contains movie titles and genres.
    ratings.csv: User ratings for each movie, including the timestamp.
    tags.csv: User-generated tags for movies, along with timestamps.
    genome_tags.csv: Additional tags assigned to movies, which provide more context for recommendation purposes.
    genome_scores.csv: Relevance scores for each genome tag per movie.
    links.csv: External IDs for movies (IMDb, TMDB).

Steps Taken
1. Setting up Neo4j

We first loaded the data into Neo4j to represent the relationships between movies, users, and tags:

    Movies were loaded as nodes, using the movies.csv file.
    Users were created from the ratings.csv file.
    Tags were generated from the tags.csv file, and relationships between users, movies, and tags were established.
    Ratings were represented as relationships between users and movies.
    Genome Tags were added using genome_tags.csv and genome_scores.csv to capture more detailed tag relationships between movies.
    External IMDb and TMDB IDs were linked to movies from the links.csv file.

2. Cypher Queries for Data Ingestion

Some of the key Cypher queries used in the project:

    Create Movie Nodes:

    cypher

LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
MERGE (m:Movie {id: toInteger(row.movieId), title: row.title, genres: row.genres});

Create User and Rating Relationships:

cypher

LOAD CSV WITH HEADERS FROM 'file:///ratings.csv' AS row
MATCH (u:User {id: toInteger(row.userId)}), (m:Movie {id: toInteger(row.movieId)})
MERGE (u)-[r:RATED {rating: toFloat(row.rating), timestamp: row.timestamp}]->(m);

Create Tag Nodes and Relationships:

cypher

LOAD CSV WITH HEADERS FROM 'file:///tags.csv' AS row
MATCH (u:User {id: toInteger(row.userId)}), (m:Movie {id: toInteger(row.movieId)})
MERGE (t:Tag {name: row.tag})
MERGE (m)-[:TAGGED_WITH]->(t)
MERGE (u)-[:TAGGED {timestamp: row.timestamp}]->(t);

Link Genome Scores to Movies:

cypher

    LOAD CSV WITH HEADERS FROM 'file:///genome_scores.csv' AS row
    MATCH (m:Movie {id: toInteger(row.movieId)}), (g:GenomeTag {id: toInteger(row.tagId)})
    MERGE (m)-[:HAS_GENOME_SCORE {relevance: toFloat(row.relevance)}]->(g);

3. Building the Frontend with Streamlit

We used Streamlit to create an interactive front-end for the recommender system. Streamlit allows users to:

    Visualize Graph Relationships: The graph data from Neo4j is displayed interactively using streamlit-agraph.
    Explore Recommendations: Users can input their movie preferences or select a movie to see similar ones based on ratings and tags.

4. Streamlit and Neo4j Integration

To connect Streamlit with Neo4j, we used the Neo4j Python driver. The driver allows us to fetch the data from the graph database and display it in the Streamlit application.
