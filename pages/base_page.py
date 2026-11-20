import allure
from playwright.sync_api import Page, expect

from config import BASE_URL


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page
        self.header_logged_in = page.locator("a:has-text('Logged in as')")
        self.header_logout = page.locator("a[href='/logout']")

    def open(self):
        with allure.step(f"Open {self.path}"):
            self.page.goto(f"{BASE_URL}{self.path}", wait_until="domcontentloaded")
        return self

    def expect_logged_in_as(self, name: str):
        expect(self.header_logged_in).to_contain_text(name)

    def logout(self):
        with allure.step("Log out"):
            self.header_logout.click()
