import base64
import os
import streamlit as st
from mistralai import Mistral, OCRResponse
from ui import app_header


def save_md(ocr_response: OCRResponse):
    md = "\n\n".join([page.markdown for page in ocr_response.pages])
    with open("output.md", "w") as f:
        f.write(md)


def save_image(base64_string, img_num):
    if "base64," in base64_string:
        base64_string = base64_string.split("base64,")[1]

    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Write the binary data to a file
    with open(f"img-{img_num}.jpeg", "wb") as file:
        file.write(image_data)


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    URL = "https://drive.google.com/uc?id=1mNEycRJoKvKlE9v7ltupP6UfnyGUSdKY"

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": URL,
        },
        include_image_base64=True,
    )

    md = "\n\n".join([page.markdown for page in ocr_response.pages])

    print(md)

    save_md(ocr_response)

    img_num = 0
    for page in ocr_response.pages:
        for image in page.images:
            # save to file
            save_image(image.image_base64, img_num)
            img_num += 1


ocr_icon = ":material/scanner:"


def mistral_ocr():
    app_header(
        icon=f":orange[{ocr_icon}]",
        title="Mistral OCR",
        description="Turn PDF or Image to Markdown with Mistral AI OCR",
    )
