import allure
import pytest
from playwright.sync_api import expect

from pages.product_page import ProductPage
from pages.products_page import ProductsPage

pytestmark = [pytest.mark.ui, allure.feature("UI: catalog")]


@pytest.mark.smoke
def test_catalog_shows_same_count_as_api(page, api):
    expected = len(api.products().body["products"])
    catalog = ProductsPage(page).open()
    expect(catalog.cards).to_have_count(expected)


def test_ui_search_matches_api_search(page, api):
    query = "top"
    api_names = sorted(p["name"].strip() for p in api.search(query).body["products"])
    catalog = ProductsPage(page).open()
    catalog.search(query)
    expect(catalog.title).to_have_text("Searched Products")
    expect(catalog.cards).to_have_count(len(api_names))
    assert sorted(catalog.names()) == api_names


def test_search_with_no_results_shows_empty_list(page):
    catalog = ProductsPage(page).open()
    catalog.search("zzz-no-such-product")
    expect(catalog.cards).to_have_count(0)


def test_product_card_matches_api_data(page, api):
    product = api.products().body["products"][0]
    card = ProductPage(page, product["id"]).open()
    expect(card.name).to_have_text(product["name"])
    expect(card.price).to_have_text(product["price"])
    expect(card.availability).to_be_visible()
