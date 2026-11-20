import re
import warnings

import allure
import pytest
from playwright.sync_api import expect

from api.client import ShopApi
from config import BLOCKED_HOSTS
from data.users import new_user

AD_HOSTS = re.compile("|".join(re.escape(h) for h in BLOCKED_HOSTS))

expect.set_options(timeout=10_000)


@pytest.fixture(scope="session")
def api() -> ShopApi:
    return ShopApi()


@pytest.fixture(scope="session")
def product_ids(api) -> list[int]:
    """Real ids from the API, so tests do not depend on hardcoded numbers."""
    ids = [p["id"] for p in api.products().body["products"]]
    assert len(ids) >= 3, "catalog is too small for cart tests"
    return ids[:3]


@pytest.fixture
def user(api):
    """Account created through the API and removed after the test."""
    data = new_user()
    resp = api.create_account(data)
    assert resp.code == 201, f"precondition failed, createAccount: {resp.body}"
    yield data
    deleted = api.delete_account(data["email"], data["password"])
    if deleted.code != 200:
        warnings.warn(f"test user {data['email']} was not deleted: {deleted.body}")


@pytest.fixture
def page(page):
    """Default pytest-playwright page with ads and consent dialogs cut off."""
    page.context.route(AD_HOSTS, lambda route: route.abort())
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
