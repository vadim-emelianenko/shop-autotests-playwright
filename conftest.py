import allure
import pytest

from api.client import ShopApi
from config import BLOCKED_HOSTS
from data.users import new_user


@pytest.fixture(scope="session")
def api() -> ShopApi:
    return ShopApi()


@pytest.fixture
def user(api):
    """Account created through the API and removed after the test."""
    data = new_user()
    resp = api.create_account(data)
    assert resp.code == 201, f"precondition failed, createAccount: {resp.body}"
    yield data
    api.delete_account(data["email"], data["password"])


@pytest.fixture
def page(page):
    """Default pytest-playwright page with ads and consent dialogs cut off."""

    def block(route):
        if any(host in route.request.url for host in BLOCKED_HOSTS):
            return route.abort()
        return route.continue_()

    page.context.route("**/*", block)
    page.set_default_timeout(15_000)
    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "page" in item.funcargs:
        pg = item.funcargs["page"]
        allure.attach(pg.screenshot(full_page=True), "screenshot", allure.attachment_type.PNG)
        allure.attach(pg.url, "url", allure.attachment_type.TEXT)
