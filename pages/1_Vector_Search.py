import streamlit as st
import logging

from embeddings import get_similar_recipes


st.title("Rewe Rezept Vector Search")

logging.basicConfig(level=logging.INFO)


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
        embedding = get_similar_recipes(prompt, True, 6)
        logging.info(embedding)
        full_response = embedding

        st.text(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
