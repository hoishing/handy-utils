# %% =================================================
import importlib
import streamlit as st
from utils import url_path

# %% ================================================= config

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


# %% ================================================= load pages


page_names = [
    "yt_transcriber",
    "mistral_ocr",
    "md2epub",
    "direct_link",
    "apn_tester",
    "rm_drm",
    "groq_models",
    "astrobro_updater",
]

pages = []

for page_name in page_names:
    module = importlib.import_module(page_name)
    pages.append(
        st.Page(
            page=module.app,
            title=module.title,
            icon=module.icon,
            url_path=url_path(module.title),
        )
    )

pg = st.navigation(pages=pages)
pg.run()
