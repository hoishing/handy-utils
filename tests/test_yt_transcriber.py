import streamlit as st
from pytest import fixture
from streamlit.testing.v1 import AppTest

url_with_caption = "https://youtube.com/shorts/uYZ4J7ctpio?si=znc1rDtst7TuaXq0"
url_without_caption = "https://youtube.com/shorts/NbY29sW7gbU?si=3xLVg6641qfLYHY6"


@fixture(scope="module")
def yt():
    return AppTest.from_file("main.py", default_timeout=100).run()


def test_with_api_key(yt: AppTest):
    assert yt.text_input(key="gemini-api-key").value is not None
    assert not yt.text_input(key="url-input").disabled


def test_no_api_key(yt: AppTest):
    yt.text_input(key="gemini-api-key").set_value("").run()
    assert yt.text_input(key="url-input").disabled


def test_transcribe_with_caption(yt: AppTest):
    yt.text_input(key="gemini-api-key").set_value(st.secrets["GEMINI_API_KEY"]).run()
    yt.text_input(key="url-input").set_value(url_with_caption).run()
    assert yt.selectbox(key="caption-lang").label == "Select the language"
    yt.selectbox(key="caption-lang").select("en").run()
    assert yt.radio(key="caption-format").label == "Select the format"
    assert "00:00:00" in yt.text_area(key="caption-output").value
    # text with punctuation added by AI
    yt.radio(key="caption-format").set_value("txt").run()
    assert "00:00:00" not in yt.text_area(key="caption-output").value


def test_transcribe_without_caption(yt: AppTest):
    yt.text_input(key="gemini-api-key").set_value(st.secrets["GEMINI_API_KEY"]).run()
    yt.text_input(key="url-input").set_value(url_without_caption).run()
    assert yt.text_area(key="transcript-output").value is not None
