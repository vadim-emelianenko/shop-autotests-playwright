import allure

from pages.base_page import BasePage


class ProductsPage(BasePage):
    path = "/products"

    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.title = page.locator(".features_items h2.title")
        self.cards = page.locator(".features_items .product-image-wrapper")
        self.card_names = page.locator(".features_items .productinfo p")

    def search(self, query: str):
        with allure.step(f"Search '{query}'"):
            self.search_input.fill(query)
            self.search_button.click()

    def names(self) -> list[str]:
        return [n.strip() for n in self.card_names.all_inner_texts()]
