import streamlit as st
import requests
import json
import logging

from const import (
    RECIPE_PROMPT_TEMPLATE,
    RECIPE_PROMPT_TEMPLATE2,
    RECIPE_PROMPT_TEMPLATE3,
    RECIPE_PROMPT_TEMPLATE4,
    RECIPE_PROMPT_TEMPLATE5,
)
from embeddings import get_similar_recipes

st.title("Rewe Rezept Bot")

logging.basicConfig(level=logging.INFO)

chat_context = None


def request_llm(prompt, context):
    return requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "leo",
            "prompt": prompt,
            "context": context,
            "options": {"temperature": 1},
        },
        stream=True,
    )


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Was möchtest du kochen?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        embedding = get_similar_recipes(prompt, True, 5)
        formatted_prompt = RECIPE_PROMPT_TEMPLATE5.format(embedding, prompt)
        logging.info("Prompt: {}".format(formatted_prompt))

        with request_llm(formatted_prompt, chat_context) as llm_response:
            if llm_response.encoding is None:
                llm_response.encoding = "utf-8"

            for line in llm_response.iter_lines(decode_unicode=True):
                if line:
                    stream_response = json.loads(line)
                    full_response += stream_response["response"] + ""
                    if "context" in stream_response:
                        chat_context = stream_response["context"]
                        chat_context = None
                    message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
