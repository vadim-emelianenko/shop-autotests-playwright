import allure
import pytest

pytestmark = [pytest.mark.api, allure.feature("API: catalog")]


@pytest.mark.smoke
def test_products_list_returns_items(api):
    resp = api.products()
    assert resp.http_status == 200
    assert resp.code == 200
    products = resp.body["products"]
    assert len(products) > 0
    for p in products:
        assert {"id", "name", "price", "brand", "category"} <= p.keys()


def test_products_have_unique_ids(api):
    ids = [p["id"] for p in api.products().body["products"]]
    assert len(ids) == len(set(ids))


def test_post_to_products_list_is_not_allowed(api):
    resp = api.post_products()
    assert resp.code == 405
    assert resp.message == "This request method is not supported."


def test_brands_list_returns_items(api):
    resp = api.brands()
    assert resp.code == 200
    assert all("brand" in b for b in resp.body["brands"])


def test_put_to_brands_list_is_not_allowed(api):
    assert api.put_brands().code == 405


@pytest.mark.parametrize("query", ["top", "jean", "tshirt"])
def test_search_returns_only_matching_products(api, query):
    resp = api.search(query)
    assert resp.code == 200
    found = resp.body["products"]
    assert found, f"nothing found for '{query}'"
    # Search also matches the category, so check name or category.
    for p in found:
        haystack = f"{p['name']} {p['category']['category']}".lower().replace("-", "")
        assert query in haystack, p


def test_search_without_parameter_is_bad_request(api):
    resp = api.search(None)
    assert resp.code == 400
    assert "search_product parameter is missing" in resp.message
