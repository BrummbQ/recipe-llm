import json
import psycopg2
import os
from pgvector.psycopg2 import register_vector

RECIPES_PATH = "scraper/rewe_recipes/recipes2.jsonl"
conn = psycopg2.connect(os.environ["DB_CONNECTION_STRING"])


def setup_db():
    cur = conn.cursor()
    # install pgvector
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()

    # Register the vector type with psycopg2
    register_vector(conn)

    # Create table to store embeddings and data
    table_create_command = """
    CREATE TABLE IF NOT EXISTS recipes (
                url text primary key, 
                body_html text,
                json_schema jsonb,
                embedding vector(384)
                );
                """

    cur.execute(table_create_command)
    cur.execute("SELECT COUNT(*) from recipes;")
    print(cur.fetchone())
    conn.commit()
    cur.close()


def read_recipes():
    # read recipes line by line
    with open(RECIPES_PATH, "r") as read_recipes:
        for line in read_recipes:
            recipe_data = json.loads(line)

            # insert data to db
            cur = conn.cursor()
            insert_sql = "INSERT INTO recipes (url, body_html, json_schema) VALUES (%s, %s, %s) ON CONFLICT (url) DO UPDATE SET body_html = EXCLUDED.body_html, json_schema = EXCLUDED.json_schema"
            insert_data = (
                recipe_data["url"],
                recipe_data["recipe_html"],
                recipe_data["recipe_schema"],
            )
            cur.execute(insert_sql, insert_data)
            conn.commit()
            cur.close()


setup_db()
read_recipes()

conn.close()
