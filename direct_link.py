# %%
import streamlit as st
from pathlib import Path
from ui import app_header, divider, main_container


def body():
    org_url = st.text_input(label="Google Drive or Github file URL")
    if not org_url:
        return

    divider()

    if org_url.startswith("https://drive.google.com"):
        file_id = org_url.split("/d/")[1].split("/view")[0]
        dl_link = f"https://drive.google.com/uc?export=download&id={file_id}"
        img_link = f"https://drive.google.com/thumbnail?id={file_id}&sz=w600"
        st.write(f":material/download: {dl_link}")
        st.write(f":material/image: {img_link}")
    elif org_url.startswith("https://github.com"):
        replaced_domain = org_url.replace("github.com", "raw.githubusercontent.com")
        removed_blob = replaced_domain.replace("/blob/", "/")
        st.write(f":material/download: {removed_blob}")
    else:
        st.error("Invalid URL")


def app():
    app_header(Path(__file__).stem)
    main_container(body)
