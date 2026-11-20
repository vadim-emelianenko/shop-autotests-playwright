import json
from dataclasses import dataclass, field

import allure
import requests

from config import API_URL, REQUEST_TIMEOUT


@dataclass
class ApiResponse:
    http_status: int
    body: dict = field(default_factory=dict)

    @property
    def code(self) -> int:
        # The demo API answers HTTP 200 and puts the real status into the body.
        return self.body.get("responseCode")

    @property
    def message(self) -> str:
        return self.body.get("message", "")


class ShopApi:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _call(self, method: str, path: str, **kwargs) -> ApiResponse:
        url = f"{self.base_url}/{path}"
        with allure.step(f"{method} {url}"):
            resp = self.session.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
            try:
                body = json.loads(resp.text)
            except ValueError:
                body = {"raw": resp.text}
            allure.attach(resp.text[:5000], "response", allure.attachment_type.JSON)
            return ApiResponse(resp.status_code, body)

    def products(self) -> ApiResponse:
        return self._call("GET", "productsList")

    def post_products(self) -> ApiResponse:
        return self._call("POST", "productsList")

    def brands(self) -> ApiResponse:
        return self._call("GET", "brandsList")

    def put_brands(self) -> ApiResponse:
        return self._call("PUT", "brandsList")

    def search(self, query: str | None) -> ApiResponse:
        data = {} if query is None else {"search_product": query}
        return self._call("POST", "searchProduct", data=data)

    def verify_login(self, email: str | None, password: str | None) -> ApiResponse:
        data = {k: v for k, v in {"email": email, "password": password}.items() if v is not None}
        return self._call("POST", "verifyLogin", data=data)

    def delete_verify_login(self) -> ApiResponse:
        return self._call("DELETE", "verifyLogin")

    def create_account(self, user: dict) -> ApiResponse:
        return self._call("POST", "createAccount", data=user)

    def delete_account(self, email: str, password: str) -> ApiResponse:
        return self._call("DELETE", "deleteAccount", data={"email": email, "password": password})

    def user_by_email(self, email: str) -> ApiResponse:
        return self._call("GET", "getUserDetailByEmail", params={"email": email})
