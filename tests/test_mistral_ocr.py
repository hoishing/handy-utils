import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from conftest import st_server_process


@pytest.fixture(scope="module", autouse=True)
def app():
    process = st_server_process("mistral_ocr.py")
    yield
    process.terminate()


def test_ui_loaded(page: Page):
    page.goto("http://localhost:9507/")
    heading = page.get_by_role("heading", name="mistral ocr")
    upload_button = page.get_by_role("button", name="browse files")
    expect(heading).to_be_visible()
    expect(upload_button).to_be_visible()


def test_file_upload(page: Page):
    page.goto("http://localhost:9507/")
    file_names = ["blower.jpg", "sample.pdf"]
    test_file_paths = [Path(__file__).parent / f for f in file_names]
    upload_button = page.get_by_role("button", name="browse files")
    with page.expect_file_chooser() as file_chooser_wrapper:
        upload_button.click()
    file_chooser = file_chooser_wrapper.value
    file_chooser.set_files(test_file_paths)

    for file_path in test_file_paths:
        zip_file_name = file_path.with_suffix(".zip").name
        element = page.get_by_role("button", name=f"download: {zip_file_name}")
        expect(element).to_be_visible(timeout=20000)
