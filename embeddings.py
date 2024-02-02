from sentence_transformers import SentenceTransformer
import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
import os
import tiktoken

model = SentenceTransformer("deutsche-telekom/gbert-large-paraphrase-cosine")

conn = psycopg2.connect(os.environ["DB_CONNECTION_STRING"])
# Register the vector type with psycopg2
register_vector(conn)


def get_embeddings(text):
    sentence_embeddings = model.encode(text)
    return sentence_embeddings


def recipe_json_to_text(data):
    recipe_text = ""
    recipe_text += f"Name: {data["name"]}\n"
    recipe_text += f"Beschreibung: {data["description"]}\n"
    recipe_text += f"Zutaten: {", ".join(data["recipeIngredient"])}\n"
    recipe_text += f"Anleitung\n"
    for instruction in data["recipeInstructions"]:
        recipe_text += f"{instruction["name"]}: {instruction["text"]}\n"
    recipe_text += f"Schlagworte: {data["keywords"]}\n"
    return recipe_text

def recipe_json_to_text_slim(data):
    recipe_text = ""
    recipe_text += f"Name: {data["name"]}\n"
    recipe_text += f"Beschreibung: {data["description"]}\n"
    recipe_text += f"Zutaten: {", ".join(data["recipeIngredient"])}\n"
    recipe_text += f"Schlagworte: {data["keywords"]}\n"
    return recipe_text

def get_similar_recipes(user_query, text_format = False, limit_results = 3):
    query_embedding = get_embeddings(user_query)
    embedding_array = np.array(query_embedding)
    cur = conn.cursor()
    # Get the most similar documents using the KNN <=> operator
    cur.execute(
        "SELECT json_schema FROM recipes ORDER BY embedding <=> %s LIMIT %s",
        (embedding_array, limit_results),
    )
    top_docs = cur.fetchall()
    formatted_docs = ""
    for row in top_docs:
        recipe_text = str(row[0]) + "\n\n"
        if text_format:
            recipe_text = recipe_json_to_text(row[0]) + "\n\n"
        formatted_docs += recipe_text
    return formatted_docs

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    if not string:
        return 0
    # Returns the number of tokens in a text string
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
