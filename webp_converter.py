import io
import streamlit as st
import zipfile
from pathlib import Path
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ui import app_header, divider, main_container


def resize_image(image: UploadedFile, target_width: int, quality: int) -> tuple[bytes, int]:
    """Resize an image to webp in target size and return as bytes"""

    try:
        img = Image.open(io.BytesIO(image.read()))
    except Exception as e:
        st.error(f"Error opening image {image.filename}: {e}")
        st.stop()

    try:
        # 1. 獲取原始尺寸
        original_width, original_height = img.size

        # 2. 計算目標高度以維持長寬比
        target_height = int((target_width / original_width) * original_height)

        # 3. 調整尺寸
        resized_img = img.resize((target_width, target_height), Image.LANCZOS)

        img_buffer = io.BytesIO()
        resized_img.save(img_buffer, format="WEBP", quality=quality)
        img_buffer.seek(0)

        return img_buffer.read(), target_height
    except Exception as e:
        st.error(f"Error resizing {image.name}: {e}")
        st.stop()


def resize_and_zip_images(images: list[UploadedFile], target_width: int, quality: int) -> bytes:
    """Resize an images to webp in target size and return a zip file as bytes"""

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for img in images:
            img_bytes, target_height = resize_image(img, target_width, quality)
            if img_bytes:
                file_name = f"{img.name}_{target_width}x{target_height}.webp"
                zipf.writestr(file_name, img_bytes)

    zip_buffer.seek(0)
    zip_bytes = zip_buffer.read()
    if zip_bytes:
        st.write()
        st.download_button(
            icon=":material/download:",
            label="webp images (.zip)",
            data=zip_bytes,
            file_name="resized_webp.zip",
            mime="application/zip",
            width="stretch",
        )


def individual_download(images: list[UploadedFile], target_width: int, quality: int):
    """Provide individual download buttons for each resized image"""
    divider()
    for image in images:
        img_path = Path(image.name)
        try:
            pil_img = Image.open(io.BytesIO(image.read()))
        except Exception as e:
            st.error(f"Error opening image: {e}")
            continue
        try:
            original_width, original_height = pil_img.size
            target_height = int((target_width / original_width) * original_height)
            resized_img = pil_img.resize((target_width, target_height), Image.LANCZOS)

            img_buffer = io.BytesIO()
            resized_img.save(img_buffer, format="WEBP", quality=quality)
            img_buffer.seek(0)

            file_name = str(img_path.with_suffix(".webp"))

            with st.container(horizontal=True):
                st.write(f"{file_name} ({target_width}x{target_height})")
                st.download_button(
                    icon=":material/download:",
                    label="",
                    data=img_buffer,
                    file_name=file_name,
                    mime="image/webp",
                )
        except Exception as e:
            st.error(f"Error resizing {image.name}: {e}")
            continue


def body():
    images = st.file_uploader(
        "Upload Images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True
    )

    c1, c2 = st.columns(2)
    quality = c1.number_input(value=80, label="WebP Quality", min_value=60, max_value=100)
    target_width = c2.number_input("Target width(px)", value=800, min_value=50, max_value=2000)

    download_option = st.radio("Download Option", ("Individual", "Zipped"), horizontal=True)

    if images:
        with st.spinner("Resizing images..."):
            if download_option == "Individual":
                individual_download(images, target_width, quality)
            else:
                resize_and_zip_images(images, target_width, quality)


def app():
    app_header(__name__)
    main_container(body)
