import streamlit as st

prompt: str = st.chat_input("Enter a prompt here")

USER = "user"
ASSISTANT = "assistant"

if prompt:
    st.chat_message(USER).write(prompt)
    st.chat_message(ASSISTANT).write(f"You wrote {prompt}")