import importlib
import streamlit as st
from pathlib import Path
from utils import url_path, page_metadata


root_dir = Path(__file__).parent

st.set_page_config(
    page_title="Handy Utilities",
    page_icon="static/handy-logo.svg",
    menu_items={
        "About": "https://github.com/hoishing/handy-utils",
        "Get help": "https://github.com/hoishing/handy-utils/issues",
    },
)

st.logo(root_dir / "static/handy-utils-banner.png")

st.html(root_dir / "style.css")


pages = []

for page_name, metadata in page_metadata.items():
    module = importlib.import_module(f"{page_name}")
    pages.append(
        st.Page(
            page=module.app,
            title=metadata["title"],
            icon=f":material/{metadata['icon']}:",
            url_path=url_path(metadata["title"]),
        )
    )

pg = st.navigation(pages=pages)
pg.run()
