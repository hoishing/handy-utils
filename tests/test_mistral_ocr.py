import pytest
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    page.goto("http://localhost:9507/")
    page.get_by_role("link", name="Mistral OCR").click()


def test_ui_loaded(page: Page):
    heading = page.get_by_role("heading", name="mistral ocr")
    upload_button = page.get_by_role("button", name="browse files")
    expect(heading).to_be_visible(timeout=2000)
    expect(upload_button).to_be_visible()


def test_file_upload(page: Page):
    file_names = ["blower.jpg", "sample.pdf"]
    assets_dir = Path("tests/assets")
    test_file_paths = [assets_dir / f for f in file_names]
    upload_button = page.get_by_role("button", name="browse files")
    with page.expect_file_chooser() as file_chooser_wrapper:
        upload_button.click()
    file_chooser = file_chooser_wrapper.value
    file_chooser.set_files(test_file_paths)

    for file_path in test_file_paths:
        zip_file_name = file_path.with_suffix(".zip").name
        element = page.get_by_role("button", name=f"download: {zip_file_name}")
        expect(element).to_be_visible(timeout=20000)
