from pathlib import Path
from playwright.sync_api import Page, expect
from pytest import fixture


@fixture(scope="function", autouse=True)
def GOTO_PAGE(page: Page):
    page.goto("http://localhost:9507/")
    page.get_by_role("link", name="Icon Resize").click()


def test_resize_and_download(page: Page):
    """
    Tests that the icon resize functionality works as expected.
    - Uploads an image.
    - Clicks the resize button.
    - Downloads the resized icons as a zip file.
    """
    # Use an existing file from the assets directory
    image_path = Path(__file__).parent / "assets" / "blower.jpg"

    # Upload the file
    file_input = page.locator('input[type="file"]')
    expect(file_input).to_be_visible()
    file_input.set_input_files(image_path)

    # Check that the file is uploaded
    expect(page.get_by_text(image_path.name)).to_be_visible()

    # Click the resize button
    resize_button = page.get_by_role("button", name="Resize and Download")
    expect(resize_button).to_be_visible()
    resize_button.click()

    # Wait for the download to start and get the download object
    with page.expect_download() as download_info:
        download_button = page.get_by_role("button", name="Download Resized Icons (.zip)")
        expect(download_button).to_be_visible(timeout=10000)
        download_button.click()
    
    download = download_info.value

    # Check if the download is successful
    assert download.failure() is None
    assert download.suggested_filename == "resized_icons.zip"
