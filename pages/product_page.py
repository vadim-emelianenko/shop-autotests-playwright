import allure

from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page, product_id: int = 1):
        super().__init__(page)
        self.path = f"/product_details/{product_id}"
        self.name = page.locator(".product-information h2")
        self.price = page.locator(".product-information span span")
        self.availability = page.locator(".product-information p:has-text('Availability')")
        self.quantity = page.locator("#quantity")
        self.add_button = page.locator("button.cart")
        self.modal = page.locator("#cartModal")
        self.view_cart_link = page.locator("#cartModal a[href='/view_cart']")
        self.continue_button = page.locator("#cartModal .close-modal")

    def add_to_cart(self, qty: int = 1):
        with allure.step(f"Add {qty} pcs to cart"):
            self.quantity.fill(str(qty))
            self.add_button.click()
            self.modal.wait_for(state="visible")

    def go_to_cart(self):
        self.view_cart_link.click()
