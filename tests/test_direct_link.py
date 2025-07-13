from playwright.sync_api import Locator, Page, expect
from pytest import fixture

google_drive_url = (
    "https://drive.google.com/file/d/1DEvagqjQN-au9wvlpXomQZ746CUR8uqd/view?usp=sharing"
)
github_url = "https://github.com/hoishing/natal/blob/main/docs/assets/favicon.png"


@fixture(scope="function", autouse=True)
def textbox(page: Page) -> Locator:
    page.goto("http://localhost:9507/")
    page.get_by_role("link", name="Direct Link").click()
    return page.get_by_role("textbox", name="Google Drive or Github file URL")


def test_google_drive_url(textbox: Locator, page: Page):
    expect(textbox).to_be_visible(timeout=2000)
    textbox.fill(google_drive_url)
    textbox.press("Enter")
    expect(
        page.get_by_role(
            "link",
            name="https://drive.google.com/uc?",
        )
    ).to_be_visible()
    expect(
        page.get_by_role(
            "link",
            name="https://drive.google.com/thumbnail?",
        )
    ).to_be_visible()


def test_github_url(textbox: Locator, page: Page):
    textbox.fill(github_url)
    textbox.press("Enter")
    expect(
        page.get_by_role("link", name="https://raw.githubusercontent")
    ).to_be_visible()


def test_invalid_url(textbox: Locator, page: Page):
    textbox.fill("asdf")
    textbox.press("Enter")
    expect(page.get_by_text("Invalid URL")).to_be_visible()
