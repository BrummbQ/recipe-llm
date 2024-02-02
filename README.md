# Recipes LLM and Embeddings

Crawl recipes from [Rewe Rezepte](https://www.rewe.de/rezeptsammlung/) and embed them into a LLM.

## Fetch data

```
# Activate python env
source venv/bin/activate
# crawl recipes
scrapy crawl recipe -o recipes2.jsonl
```

## Setup db

```
# run db container
docker-compose up -d
# prepare db
DB_CONNECTION_STRING="postgres://postgres:test@localhost:5432/postgres" python3 read_recipes.py
# setup embeddings
DB_CONNECTION_STRING="postgres://postgres:test@localhost:5432/postgres" python3 calculate_embeddings.py
```

## Setup LLM

I used the [Ollama app](https://ollama.ai) on a macbook M1.

```
# setup model
ollama create leo -f Modelfile-leo
# start ollama
ollama serve
```

### German Model

https://github.com/jphme/EM_German/blob/main/README.md

## Run chatbot

Now you can start the chatbot interface. A browser window should open

```
DB_CONNECTION_STRING="postgres://postgres:test@localhost:5432/postgres" streamlit run recipes_ui.py
```

### Vector Search Examples

- Vegetarischer Burger mit Nüssen
- pesto nudeln mit fisch
- Japanisches Nudelgericht vegetarisch

### Recipe LLM Examples

- Ich habe Kartoffeln, Möhren und einen Backofen. Was soll ich essen?
- Gib mir das Rezept für Backfisch mit kartoffeln
- Meine Kinder haben Hunger und ich keine Zeit. Wie bekomme ich sie satt?
- Erstelle eine Einkaufsliste für Obstsalat mit süßen früchten
- Welche Frucht kann ich anstelle einer Melone benutzen?
- Das Arbeitsamt hat mir mein Geld gekürzt. Welche Gerichte sind günstig?
- Getränke für Männer
- Getränke für Frauen
- Getränke für kleine/große Menschen
