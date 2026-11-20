import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

pytestmark = [pytest.mark.ui, allure.feature("UI: cart")]


@pytest.mark.smoke
def test_added_product_appears_in_cart(page, product_ids):
    product = ProductPage(page, product_ids[0]).open()
    name = product.name.inner_text()
    product.add_to_cart()
    product.go_to_cart()
    cart = CartPage(page)
    expect(cart.rows).to_have_count(1)
    expect(cart.name()).to_have_text(name)


@pytest.mark.parametrize("qty", [1, 4, 10])
def test_cart_total_equals_price_times_quantity(page, qty, product_ids):
    product = ProductPage(page, product_ids[1]).open()
    product.add_to_cart(qty)
    product.go_to_cart()
    cart = CartPage(page)
    expect(cart.quantity()).to_have_text(str(qty))
    expect(cart.total()).to_have_text(f"Rs. {cart.price_value() * qty}")


def test_same_product_added_twice_sums_quantity(page, product_ids):
    product = ProductPage(page, product_ids[2]).open()
    product.add_to_cart(2)
    product.continue_shopping()
    product.add_to_cart(3)
    product.go_to_cart()
    cart = CartPage(page)
    expect(cart.rows).to_have_count(1)
    expect(cart.quantity()).to_have_text("5")


def test_removed_product_disappears_from_cart(page, product_ids):
    product = ProductPage(page, product_ids[0]).open()
    product.add_to_cart()
    product.go_to_cart()
    cart = CartPage(page)
    cart.remove()
    expect(cart.rows).to_have_count(0)
    expect(cart.empty_message).to_be_visible()


def test_cart_survives_login(page, product_ids, user):
    """Guest cart must stay after the user logs in."""
    product = ProductPage(page, product_ids[0]).open()
    name = product.name.inner_text()
    product.add_to_cart(2)
    LoginPage(page).open().login(user["email"], user["password"])
    cart = CartPage(page).open()
    expect(cart.rows).to_have_count(1)
    expect(cart.name()).to_have_text(name)
    expect(cart.quantity()).to_have_text("2")
