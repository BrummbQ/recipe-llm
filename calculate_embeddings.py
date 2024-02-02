import psycopg2
import os
from pgvector.psycopg2 import register_vector
import logging

from const import ALTER_TABLE_SQL, DELETE_EMBEDDINGS_SQL, UPDATE_EMBEDDING_SQL
from embeddings import get_embeddings, recipe_json_to_text_slim


logging.basicConfig(level=logging.INFO)


SCHEMA_KEYS = [
    "description",
    "name",
    "keywords",
    "recipeIngredient",
    "recipeInstructions",
    "recipeCategory",
]

conn = psycopg2.connect(os.environ["DB_CONNECTION_STRING"])
# Register the vector type with psycopg2
register_vector(conn)


def setup_embeddings():
    cur = conn.cursor()
    update_cur = conn.cursor()

    cur.execute(DELETE_EMBEDDINGS_SQL)
    cur.execute(ALTER_TABLE_SQL)
    cur.execute("SELECT url, json_schema FROM recipes;")

    while True:
        rows = cur.fetchmany(100)
        if not rows:
            break

        for row in rows:
            write_embedding(update_cur, row)

    cur.close()
    update_cur.close()


def write_embedding(update_cur, row):
    data_url = row[0]
    data_json = row[1]
    data_text = recipe_json_to_text_slim(data_json)

    # calculate embeddings
    sentence_embeddings = get_embeddings(data_text)

    # write embeddings to db
    logging.info("Write embedding: %s %s", data_url, data_text)
    update_cur.execute(UPDATE_EMBEDDING_SQL, (sentence_embeddings, data_url))
    conn.commit()


setup_embeddings()

conn.close()
