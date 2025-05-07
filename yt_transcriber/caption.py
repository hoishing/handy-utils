import streamlit as st
from google.genai import Client, types
from pytubefix import YouTube


def add_punctuation(api_key: str, transcript: str) -> str:
    """Add punctuation to a transcript using Gemini's LLM."""
    sys_prompt = "add punctuation to the following text, just output the text with punctuation, no other text"
    client = Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        config=types.GenerateContentConfig(system_instruction=sys_prompt),
        contents=transcript,
    )
    return response.text


def caption_ui(yt: YouTube | None, langs: list[str], api_key: str) -> None:
    st.markdown("#### 💬 &nbsp; Extract Captions")

    lang = st.selectbox(
        label="Select the language",
        options=langs,
        index=None,
        format_func=lambda x: x.split(".")[-1]
    )

    format = st.radio(
        label="Select the format",
        options=["srt", "txt"],
        index=0,
        horizontal=True,
        disabled=not lang,
    )

    transcript = ""
    if lang:
        if format == "srt":
            transcript = yt.captions[lang].generate_srt_captions()
        elif format == "txt":
            raw_transcript = yt.captions[lang].generate_txt_captions()
            transcript = add_punctuation(api_key, raw_transcript)

    st.text_area(
        label="Captions", value=transcript, height=400, disabled=not transcript
    )
