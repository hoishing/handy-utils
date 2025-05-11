import streamlit as st
from direct_link import direct_link, direct_link_icon
from list_groq_models import groq_models, models_icon
from mistral_ocr import mistral_ocr, ocr_icon
from yt_transcriber import yt_icon, yt_transcriber

st.set_page_config(
    page_title="Handy Utilities",
    page_icon="static/handy-logo.svg",
    menu_items={
        "About": "https://github.com/hoishing/handy-utils",
        "Get help": "https://github.com/hoishing/handy-utils/issues",
    },
)

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
page4 = st.Page(
    direct_link,
    title="Direct Link",
    icon=direct_link_icon,
)

pg = st.navigation([page1, page2, page3, page4])
pg.run()
