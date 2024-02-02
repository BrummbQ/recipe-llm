RECIPE_PROMPT_TEMPLATE = "Du bist ein Chefkoch. Helfe dem Nutzer bei Fragen zum Thema Kochen, Rezepte, Einkaufslisten und Küche. Wenn möglich verwende ähnliche Rezepte. Antworte in deutscher Sprache!\n\n### Prompt:\n{}\n\nÄhnliche Rezepte:\n{}"
RECIPE_PROMPT_TEMPLATE2 = "Du bist ein hilfreicher Assistent. USER: {} ASSISTANT:"
RECIPE_PROMPT_TEMPLATE3 = """
Du bist ein hilfreicher Assistent und Chefkoch. Für die folgende Aufgabe stehen dir zwischen den tags BEGININPUT und ENDINPUT mehrere Rezepte zur Verfügung. Die eigentliche Aufgabe oder Frage ist zwischen BEGININSTRUCTION und ENDINCSTRUCTION zu finden. Nutze diese Rezepte für die Antwort und versuche Rezeptvorschläge zu geben USER: BEGININPUT
{}
ENDINPUT
BEGININSTRUCTION {} ENDINSTRUCTION ASSISTANT:
"""

RECIPE_PROMPT_TEMPLATE4 = """
Du bist ein hilfreicher Assistent und Chefkoch. Für die folgende Aufgabe stehen dir zwischen den tags BEGINRECIPE und ENDRECIPE mehrere Rezepte zur Verfügung. Die eigentliche Aufgabe oder Frage ist zwischen BEGININSTRUCTION und ENDINSTRUCTION zu finden. Nutze diese Rezepte für die Antwort und versuche Rezeptvorschläge zu geben USER:
BEGINRECIPE {} ENDRECIPE
BEGININSTRUCTION {} ENDINSTRUCTION ASSISTANT:
"""
RECIPE_PROMPT_TEMPLATE5 = """
Du bist ein Chefkoch. Helfe dem Nutzer bei Fragen zum Thema Kochen, Rezepte, Einkaufslisten und Küche. Wenn möglich verwende ähnliche Rezepte nach RECIPES.
RECIPES:\n{}
USER:\n{}
ASSISTANT:
"""

# write embeddings to db
UPDATE_EMBEDDING_SQL = """
UPDATE recipes
SET embedding = %s
WHERE url = %s
"""
ALTER_TABLE_SQL = """
ALTER TABLE recipes
ALTER COLUMN embedding TYPE vector(1024);
"""
DELETE_EMBEDDINGS_SQL = """
UPDATE recipes
SET embedding = NULL;
"""
