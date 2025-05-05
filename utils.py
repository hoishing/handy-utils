import streamlit as st

sess = st.session_state


def get_api_key(brand: str) -> str | None:
    """Get API key from session state or secrets.toml otherwise return None"""
    key_name = f"{brand.upper()}_API_KEY"

    if key_name in sess:
        return sess[key_name]

    try:
        sess[key_name] = st.secrets[key_name]
        return sess[key_name]
    except Exception:
        return None
