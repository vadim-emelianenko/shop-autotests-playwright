import re

import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.feature("UI: auth")]


@pytest.mark.smoke
def test_login_with_account_created_by_api(page, user):
    login = LoginPage(page).open()
    login.login(user["email"], user["password"])
    login.expect_logged_in_as(user["name"])


def test_login_with_wrong_password_shows_error(page, user):
    login = LoginPage(page).open()
    login.login(user["email"], "wrong-password")
    expect(login.error).to_have_text("Your email or password is incorrect!")
    expect(login.header_logged_in).to_have_count(0)


def test_logout_returns_to_login_page(page, user):
    login = LoginPage(page).open()
    login.login(user["email"], user["password"])
    login.logout()
    expect(page).to_have_url(re.compile(r"/login$"))
    expect(login.header_logged_in).to_have_count(0)


def test_signup_with_existing_email_shows_error(page, user):
    login = LoginPage(page).open()
    login.start_signup("Someone", user["email"])
    expect(login.signup_error).to_have_text("Email Address already exist!")
