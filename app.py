from dataclasses import dataclass

import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


@dataclass
class Message:
    actor: str
    payload: str


@st.cache_resource
def get_llm() -> OpenAI:
    return OpenAI()


def get_llm_chain():
    template = """Answer the question based on the context below and use the history of the conversation to continue
                If the question cannot be answered using the information provided answer with "I don't know"
                              
                Context:
                You are deeply knowledgeable about all the National Parks in the United states and you want to 
                suggest the parks to visit based on the question.
                              
                History of the conversation:
                {chat_history}
                
                Question: 
                {question}

                Answer: 
    """
    prompt_template = PromptTemplate.from_template(template)
    # Notice that we need to align the `memory_key`
    memory = ConversationBufferMemory(memory_key="chat_history")
    chain = LLMChain(
        llm=get_llm(),
        prompt=prompt_template,
        verbose=True,
        memory=memory
    )
    return chain


USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"


def initialize_session_state():
    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = \
            [Message(
                actor=ASSISTANT,
                payload="""Great to hear that you wish to visit a national park. 
                You can ask me anything about what could be great places to visit
                """)]
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
