import os
import streamlit as st

sess = st.session_state

page_metadata = {
    "token_counter": {
        "title": "Token Counter",
        "color": "violet",
        "icon": "assignment",
        "description": "Count tokens used in a text for different LLM models",
        "youtube": "https://youtu.be/gfKEGCvUJbQ",
    },
    "mistral_ocr": {
        "title": "Mistral OCR",
        "color": "orange",
        "icon": "scanner",
        "description": "Turn PDF or Image to Markdown with Mistral AI OCR",
        "youtube": "https://youtu.be/NGe5YIqdYQQ",
    },
    "md2epub": {
        "title": "MD to EPUB",
        "color": "violet",
        "icon": "markdown",
        "description": "Convert markdown with images to epub",
        "youtube": "https://youtu.be/X3eKrTwfYHw",
    },
    "direct_link": {
        "title": "Direct Link",
        "color": "blue",
        "icon": "link",
        "description": "Get direct media file link from Google Drive or Github",
        "youtube": "https://youtu.be/1v-viXpOY2g",
    },
    "apn_tester": {
        "title": "APNs Tester",
        "color": "blue",
        "icon": "mark_chat_unread",
        "description": "Test Apple Push Notification With Ease",
        "youtube": "https://youtu.be/ZocYEKC9rSA",
    },
    "rm_drm": {
        "title": "Remove DRM",
        "color": "orange",
        "icon": "key",
        "description": "Remove DRM of Your Own Ebook from Adobe Digital Edition",
        "youtube": "https://youtu.be/frNyHMN4_e4",
    },
    "groq_models": {
        "title": "Groq Models",
        "color": "orange",
        "icon": "lightbulb",
        "description": "List all currently active and available models in Groq",
        "youtube": "https://youtu.be/CO8QFJhJ2Z8",
    },
    "pypi_name_checker": {
        "title": "PyPI Name Checker",
        "color": "blue",
        "icon": "check_circle",
        "description": "Check the availability of PyPi package names",
        "youtube": "https://youtu.be/SRdoIzs6N3k",
    },
    "icon_resize": {
        "title": "Icon Resize",
        "color": "green",
        "icon": "photo_size_select_small",
        "description": "Resize icon to various sizes",
        "youtube": "https://youtu.be/3enxU_c3hzg",
    },
    # "astrobro_updater": {
    #     "title": "Astrobro Updater",
    #     "color": "orange",
    #     "icon": "planet",
    #     "description": "Update [Astrobro](https://hoishing.github.io/astrobro/) JSON files with city names and country codes",
    #     "youtube": "",
    # },
}


def get_api_key(brand: str) -> str | None:
    """Get API key from session state or environment variable otherwise return None"""
    key_name = f"{brand.upper()}_API_KEY"

    if key_name in sess:
        return sess[key_name]

    if value := os.environ.get(key_name):
        sess[key_name] = value
        return value
    return None


def url_path(title: str) -> str:
    """convert utility title to url path"""
    return title.lower().replace(" ", "_")


def get_page_info(page_key: str) -> tuple[str, str, str]:
    """Get page metadata (title, colored_icon, description) for a given page key"""
    if page_key not in page_metadata:
        raise KeyError(f"Page key '{page_key}' not found in page_metadata")

    metadata = page_metadata[page_key]
    title = metadata["title"]
    color = metadata["color"]
    icon = metadata["icon"]
    description = metadata["description"]

    colored_icon = f":{color}[material/{icon}]:"

    return title, colored_icon, description
