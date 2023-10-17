from dataclasses import dataclass

import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


@dataclass
class Message:
    actor: str
    payload: str


@st.cache_resource
def get_llm() -> VertexAI:
    return VertexAI(model_name="text-bison@001")


def get_llm_chain():
    template = """You are a nice chatbot having a conversation with a human.

    Previous conversation:
    {chat_history}

    New human question: {question}
    Response:"""
    prompt_template = PromptTemplate.from_template(template)
    # Notice that we need to align the `memory_key`
    memory = ConversationBufferMemory(memory_key="chat_history")
    conversation = LLMChain(
        llm=get_llm(),
        prompt=prompt_template,
        verbose=True,
        memory=memory
    )
    return conversation


USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"


def initialize_session_state():
    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi!How can I help you?")]
    if "llm_chain" not in st.session_state:
        st.session_state["llm_chain"] = get_llm_chain()


def get_llm_chain_from_session() -> LLMChain:
    return st.session_state["llm_chain"]


initialize_session_state()

msg: Message
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

prompt: str = st.chat_input("Enter a prompt here")

if prompt:
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)

    with st.spinner("Please wait.."):
        llm_chain = get_llm_chain_from_session()
        response: str = llm_chain({"question": prompt})["text"]
        st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
        st.chat_message(ASSISTANT).write(response)
