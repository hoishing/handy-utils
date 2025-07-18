import streamlit as st
from google import genai
from transformers import AutoTokenizer
from ui import api_key_input, app_header, divider, main_container

MODELS = {
    "Google": [
        "gemini-2.5-flash",
        "gemma-3n-e4b-it",
    ],
    "HuggingFace": [
        "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
        "meta-llama/Llama-3.3-70B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "qwen/qwen3-32b",
    ],
}


def counter(provider: str, model: str, api_key: str, content: str) -> int:
    try:
        match provider:
            case "Google":
                client = genai.Client(api_key=api_key)
                response = client.models.count_tokens(model=model, contents=content)
                return response.total_tokens
            case "HuggingFace":
                tokenizer = AutoTokenizer.from_pretrained(model, api_key=api_key)
                tokens = tokenizer.encode(content)
                return len(tokens)
    except Exception as e:
        st.error(e.__dict__["message"])


def model_chooser(provider: str, content: str):
    api_key = api_key_input(provider)

    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    model = c1.selectbox("Select a model", MODELS[provider])
    if c2.button(
        "Count tokens",
        use_container_width=True,
        key=f"{provider}_counter",
        disabled=not api_key,
    ):
        if token_count := counter(provider, model, api_key, content):
            st.markdown(f":violet-badge[:material/token: tokens] {token_count}")


def body():
    st.markdown(
        """
        ##### 📜 &nbsp; Notes

        - HuggingFace models need to request permission before use.
        - Groq uses opensource models that similar to those in HuggingFace.
        - [AutoTokenizer](https://huggingface.co/docs/transformers/en/main_classes/tokenizer) is used for HuggingFace models.
        - [CountTokens API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/count-tokens) is used for Google models.
        """
    )
    divider()
    content = st.text_area("Enter your text", height=300)
    tabs = zip(MODELS.keys(), st.tabs(MODELS.keys()))
    for provider, tab in tabs:
        with tab:
            model_chooser(provider, content)


def app():
    app_header(__name__)
    main_container(body)
