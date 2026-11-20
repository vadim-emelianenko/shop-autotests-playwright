import allure

from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/view_cart"

    def __init__(self, page):
        super().__init__(page)
        self.rows = page.locator("#cart_info_table tbody tr[id^='product-']")
        self.empty_message = page.locator("#empty_cart")

    def row(self, index: int = 0):
        return self.rows.nth(index)

    def name(self, index: int = 0):
        return self.row(index).locator(".cart_description h4")

    def quantity(self, index: int = 0):
        return self.row(index).locator(".cart_quantity button")

    def total(self, index: int = 0):
        return self.row(index).locator(".cart_total_price")

    def price_value(self, index: int = 0) -> int:
        return money(self.row(index).locator(".cart_price p").inner_text())

    def remove(self, index: int = 0):
        with allure.step(f"Remove row #{index}"):
            self.row(index).locator(".cart_quantity_delete").click()


def money(text: str) -> int:
    # "Rs. 500" -> 500
    return int("".join(ch for ch in text if ch.isdigit()))
