import pytest
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    page.goto("http://localhost:9507/")
    page.get_by_role("link", name="MD to EPUB").click()


def test_ui_loaded(page: Page):
    heading = page.get_by_role("heading", name="md to epub")
    upload_button = page.get_by_role("button", name="browse files")
    expect(heading).to_be_visible(timeout=2000)
    expect(upload_button).to_be_visible()


def test_file_upload(page: Page):
    asset_path = Path("tests/assets/sample.zip")
    upload_button = page.get_by_role("button", name="browse files")
    with page.expect_file_chooser() as file_chooser_wrapper:
        upload_button.click()
    file_chooser = file_chooser_wrapper.value
    file_chooser.set_files(asset_path)
    expect(page.get_by_role("button", name="download epub")).to_be_visible()
