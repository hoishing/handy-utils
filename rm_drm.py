# %% =================================================
import streamlit as st
from deDRM.adobekey import extract_adobe_key
from deDRM.ineptepub import decryptBook as decrypt_epub
from deDRM.ineptpdf import decryptBook as decrypt_pdf
from io import BytesIO
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ui import app_header, main_container

icon = ":material/key:"
title = "Remove DRM"


# %% ================================================= decrypt file


def decrypt_file(encrypted_file: UploadedFile, dat_file: UploadedFile) -> BytesIO:
    # Extract the Adobe key
    adobe_key = extract_adobe_key(dat_file.getvalue())

    if encrypted_file.name.lower().endswith(".pdf"):
        return decrypt_pdf(adobe_key, encrypted_file)
    elif encrypted_file.name.lower().endswith(".epub"):
        return decrypt_epub(adobe_key, encrypted_file)
    else:
        raise ValueError("Unsupported file type")


# %% ================================================= app


def body():
    st.write("#### Remove DRM ")

    mime_types = {"pdf": "application/pdf", "epub": "application/epub+zip"}
    book_data = file_name = ""
    mime = mime_types["epub"]

    key_file = st.file_uploader(
        "Activation file",
        type="dat",
        help="~/Library/Application Support/Adobe/Digital Editions/activation.dat\n\nOnly Digital Edition for macOS is supported",
    )

    encrypted_file = st.file_uploader("epub or pdf file", type=["epub", "pdf"])

    if encrypted_file and key_file:
        book_data = decrypt_file(encrypted_file, key_file)
        file_name = encrypted_file.name
        mime = mime_types[encrypted_file.name.split(".")[-1]]

    st.write("")

    st.download_button(
        label="Download",
        data=book_data,
        file_name=file_name,
        mime=mime,
        disabled=not book_data,
    )


def app():
    app_header(
        icon=f":orange[{icon}]",
        title=title,
        description="remove DRM of your own ebook in Adobe Digital Edition",
    )
    main_container(body)


# %% ================================================= old app
