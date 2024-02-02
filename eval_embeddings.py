from sentence_transformers import SentenceTransformer, util
import psycopg2
import os

from embeddings import num_tokens_from_string, recipe_json_to_text_slim

query = "Ich möchte gesunden Salat"
models = [
    "multi-qa-distilbert-cos-v1",
    "msmarco-distilbert-cos-v5",
    "multi-qa-mpnet-base-cos-v1",
    "multi-qa-MiniLM-L6-cos-v1",
    "multi-qa-MiniLM-L6-dot-v1",
    "multi-qa-mpnet-base-dot-v1",
    "distiluse-base-multilingual-cased-v1",
    "deutsche-telekom/gbert-large-paraphrase-cosine",
]
for m in models:
    model = SentenceTransformer(m)
    # model.max_seq_length = 512

    conn = psycopg2.connect(os.environ["DB_CONNECTION_STRING"])
    cur = conn.cursor()

    # Get recipes list
    cur.execute("SELECT json_schema FROM recipes LIMIT 3;")
    res = cur.fetchall()
    sentences1 = []
    sentences2 = []

    for r in res:
        sentences1.append(recipe_json_to_text_slim(r[0]))

    # print(sentences1)
    for r in sentences1:
        c = len(r.split())
        sentences2.append(query)
        print(f"token: {num_tokens_from_string(r)} words: {c}")

    # Compute embedding for both lists
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    # Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    # cosine_scores = util.dot_score(embeddings1, embeddings2)

    # Output the pairs with their score
    for i in range(len(sentences1)):
        print(
            "{} \t\t {} \t\t Score: {:.4f}".format(
                sentences1[i][:13], sentences2[i], cosine_scores[i][i]
            )
        )

    print(f"Model: {m} Max Sequence Length: {model.max_seq_length}")
