import allure

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page):
        super().__init__(page)
        self.email = page.locator("[data-qa='login-email']")
        self.password = page.locator("[data-qa='login-password']")
        self.submit = page.locator("[data-qa='login-button']")
        self.error = page.locator("form[action='/login'] p")
        self.signup_name = page.locator("[data-qa='signup-name']")
        self.signup_email = page.locator("[data-qa='signup-email']")
        self.signup_button = page.locator("[data-qa='signup-button']")
        self.signup_error = page.locator("form[action='/signup'] p")

    def login(self, email: str, password: str):
        with allure.step(f"Log in as {email}"):
            self.email.fill(email)
            self.password.fill(password)
            self.submit.click()

    def start_signup(self, name: str, email: str):
        with allure.step(f"Start signup for {email}"):
            self.signup_name.fill(name)
            self.signup_email.fill(email)
            self.signup_button.click()
