# %% =================================================
import streamlit as st
from deDRM.adobekey import extract_adobe_key
from deDRM.ineptepub import decryptBook as decrypt_epub
from deDRM.ineptpdf import decryptBook as decrypt_pdf
from io import BytesIO
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ui import app_header, divider, main_container

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
    st.markdown(
        """
        #### 🧑‍💻 Usage

        - only Adobe Digital Edition(ADE) for macOS is supported
        - export the ebook as `acsm` file from Google Play Books
        - import the `acsm` file to ADE
        - right click the ebook in ADE and click `Show File in Finder`
        - upload the drm-protected epub/pdf file from Finder
        - upload the activation file from ADE
            - `~/Library/Application Support/Adobe/Digital Editions/activation.dat`
        - download the decrypted epub/pdf file
        """
    )

    divider()

    mime_types = {"pdf": "application/pdf", "epub": "application/epub+zip"}
    book_data = file_name = ""
    mime = mime_types["epub"]

    encrypted_file = st.file_uploader("epub or pdf file", type=["epub", "pdf"])
    key_file = st.file_uploader("Activation file", type="dat")

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
    app_header(__name__)
    main_container(body)
