# shop-autotests-playwright

UI and API tests for [Automation Exercise](https://automationexercise.com), a public demo shop.
Python, Playwright, pytest, requests, Docker, GitHub Actions, Allure.

[![tests](https://github.com/vadim-emelianenko/shop-autotests-playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/vadim-emelianenko/shop-autotests-playwright/actions/workflows/tests.yml)

Allure report, published after runs on main: https://vadim-emelianenko.github.io/shop-autotests-playwright/

## Run

```bash
make test
```

Needs Docker. Without Docker:

```bash
pip install -r requirements-dev.txt && playwright install chromium && pytest
```

`pytest -m smoke` runs the critical subset, `pytest -m api` runs API tests only, `-n 4` runs them in 4 workers.

## Coverage

| Area | Checks |
|---|---|
| API catalog | product and brand lists, search, wrong HTTP methods, missing parameters |
| API accounts | create, login check, user details, duplicate email, deleted user can not log in |
| UI auth | login with a user created through the API, wrong password, logout, signup with a taken email |
| UI catalog | catalog size equals the API list, search, empty search, product card vs API data |
| UI cart | add, quantities summed, price times quantity, remove, cart kept after login |

## Structure

```
api/client.py      requests wrapper, each call is an Allure step
pages/             Page Objects, all UI locators
data/users.py      unique test users (Faker)
conftest.py        fixtures: API client, catalog, test user, page without ads
tests/api, tests/ui
```

Test users are created through the API and deleted after each test. UI tests take expected values from the API instead of constants.

Ad and consent hosts are blocked in the browser, on the demo site their popups cover buttons.

The API answers HTTP 200 to everything. The real status is in the `responseCode` field, and that is what the tests check.

CI: lint first, tests only after it passes. A pull request gets the smoke subset, push to main and the daily run at 06:00 UTC get everything. A manual run accepts a marker expression and the number of workers. Results of each test are shown on the run page and in the pull request. The report goes to the `gh-pages` branch, a failed test also leaves a Playwright trace in the build artifacts.

## Found while testing

In one of the first CI runs `GET /api/productsList` answered without the `products` key. API tests keep failing on that, UI tests retry the request before they start.
