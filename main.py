import streamlit as st
from list_groq_models import groq_models, models_icon
from mistral_ocr import mistral_ocr, ocr_icon
from yt_transcriber import yt_icon, yt_transcriber

PAGE_CONFIG = dict(
    page_title="Handy Utilities",
    page_icon="static/handy-logo.svg",
    menu_items={
        "About": "https://github.com/hoishing/handy-utils",
        "Get help": "https://github.com/hoishing/handy-utils/issues",
    },
)
st.set_page_config(**PAGE_CONFIG)

st.logo("static/handy-utils-banner.png")

st.html("style.css")

page1 = st.Page(
    yt_transcriber,
    title="Youtube Transcriber",
    icon=yt_icon,
    default=True,
)
page2 = st.Page(
    mistral_ocr,
    title="Mistral OCR",
    icon=ocr_icon,
)
page3 = st.Page(
    groq_models,
    title="Groq Models",
    icon=models_icon,
)

pg = st.navigation([page1, page2, page3])
pg.run()
