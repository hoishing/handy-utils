import direct_link
import groq_models
import md2epub
import mistral_ocr
import streamlit as st
import yt_transcriber
from utils import url_path

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
    page=yt_transcriber.app,
    title=yt_transcriber.title,
    icon=yt_transcriber.icon,
    url_path=url_path(yt_transcriber.title),
    default=True,
)
page2 = st.Page(
    page=mistral_ocr.app,
    title=mistral_ocr.title,
    icon=mistral_ocr.icon,
    url_path=url_path(mistral_ocr.title),
)
page3 = st.Page(
    groq_models.app,
    title=groq_models.title,
    icon=groq_models.icon,
    url_path=url_path(groq_models.title),
)
page4 = st.Page(
    direct_link.app,
    title=direct_link.title,
    icon=direct_link.icon,
    url_path=url_path(direct_link.title),
)
page5 = st.Page(
    page=md2epub.app,
    title=md2epub.title,
    icon=md2epub.icon,
    url_path=url_path(md2epub.title),
)

pg = st.navigation(
    [
        page1,
        page2,
        page3,
        page4,
        page5,
    ]
)
pg.run()
