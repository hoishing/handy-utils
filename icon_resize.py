import io
import re
import streamlit as st
import zipfile
from pathlib import Path
from PIL import Image
from ui import app_header, divider, main_container


def resize_and_zip_images(
    src_image_bytes: bytes, src_image_name: str, sizes: list[str]
) -> bytes:
    """Resize an image to different sizes and return a zip file as bytes"""
    src_path = Path(src_image_name)
    name_arr = re.split(r"(\d+)", src_path.name)
    name = name_arr[0] if len(name_arr) > 1 else src_path.stem

    try:
        img = Image.open(io.BytesIO(src_image_bytes))
    except Exception as e:
        st.error(f"Error opening image: {e}")
        return b""

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for size_str in sizes:
            try:
                size = int(size_str)
                resized_img = img.resize((size, size))

                img_buffer = io.BytesIO()
                img_format = img.format or "PNG"
                resized_img.save(img_buffer, format=img_format)
                img_buffer.seek(0)

                file_name = f"{name}_{size}{src_path.suffix}"
                zipf.writestr(file_name, img_buffer.read())
            except ValueError:
                st.warning(f"Invalid size '{size_str}' skipped.")
                continue
            except Exception as e:
                st.error(f"Error resizing image to {size_str}x{size_str}: {e}")
                continue

    zip_buffer.seek(0)
    return zip_buffer.read()


def body():
    uploaded_file = st.file_uploader(
        "Upload an icon", type=["png", "jpg", "jpeg", "webp"]
    )
    sizes_str = st.text_input("Enter desired sizes (comma-separated)", "256, 128, 64")

    if uploaded_file and sizes_str:
        sizes = [s.strip() for s in sizes_str.split(",") if s.strip().isdigit()]
        if not sizes:
            st.warning("Please enter at least one valid integer size.")
            return

        with st.spinner("Resizing images..."):
            zip_bytes = resize_and_zip_images(
                uploaded_file.getvalue(), uploaded_file.name, sizes
            )
            if zip_bytes:
                divider()
                st.download_button(
                    label="Download Resized Icons (.zip)",
                    data=zip_bytes,
                    file_name="resized_icons.zip",
                    mime="application/zip",
                )


def app():
    app_header(__name__)
    main_container(body)
