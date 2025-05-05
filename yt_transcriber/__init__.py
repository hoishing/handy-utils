import streamlit as st
from .caption import caption_ui
from .transcribe import transcribe_ui
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError
from ui import api_key_input, app_header, divider, main_container

yt_icon = ":material/youtube_activity:"


def youtube_obj(url: str | None) -> YouTube | None:
    if not url:
        return None

    try:
        yt = YouTube(url)
        yt.check_availability()
        return yt
    except RegexMatchError:
        st.error("Invalid URL")
        return None


def body():
    api_key = api_key_input("Gemini")
    url = st.text_input("Youtube URL", key="url-input", disabled=not api_key)

    yt = youtube_obj(url)
    langs = [c.code for c in yt.captions] if yt else []

    divider(key=1)

    if langs or not yt:
        caption_ui(yt, langs, api_key)
    else:
        transcribe_ui(yt, api_key)


def yt_transcriber():
    app_header(
        icon=f":red[{yt_icon}]",
        title="Youtube Transcriber",
        description="Extract captions if available, transcribe the audio with AI otherwise",
    )

    main_container(body)
