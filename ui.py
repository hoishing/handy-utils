import streamlit as st
from typing import Callable, Literal, get_args
from utils import get_api_key

LLM = Literal["Gemini", "Groq", "Mistral"]
LLM_SITES = [
    "https://ai.google.dev/gemini-api/docs/api-key",
    "https://console.groq.com/docs/quickstart",
    "https://docs.mistral.ai/getting-started/quickstart/",
]


def app_header(icon: str, title: str, description: str):
    with st.container(key="app-header"):
        st.markdown(f"## {icon} &nbsp; {title}")
        st.caption(description)


def main_container(body: Callable):
    with st.container(border=True, key="main-container"):
        body()


def divider(key: int = 1):
    with st.container(key=f"divider{key}"):
        st.divider()


def api_key_input(llm: LLM):
    api_key_docs = dict(zip(get_args(LLM), LLM_SITES))
    return st.text_input(
        f"{llm} API key",
        key=f"{llm.lower()}-api-key",
        type="password",
        value=get_api_key(llm),
        help=f"Visit [{llm}]({api_key_docs[llm]}) to get the API key",
    )
