# shop-autotests-playwright

UI and API tests for [Automation Exercise](https://automationexercise.com), a public demo shop.
Python, Playwright, pytest, requests, Docker, GitHub Actions, Allure.

[![tests](https://github.com/vadim-emelianenko/shop-autotests-playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/vadim-emelianenko/shop-autotests-playwright/actions/workflows/tests.yml)

Allure report from the last run on main: https://vadim-emelianenko.github.io/shop-autotests-playwright/

## Run

```bash
make test
```

Needs Docker. Without Docker:

```bash
pip install -r requirements.txt && playwright install chromium && pytest
```

`pytest -m smoke` runs the critical subset, `pytest -m api` runs API tests only.

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
conftest.py        API client, product ids from the API, user created by API and deleted after the test,
                   page with ad hosts blocked, screenshot on failure
tests/api, tests/ui
```

Test users are created through the API, so UI tests do not spend time on the signup form. Expected values come from the API where possible, not from constants. Ad and consent hosts are blocked because their popups cover buttons on the demo site. The API returns HTTP 200 for everything and puts the real status into `responseCode`, tests check that field.

CI runs on push to main, on pull requests and once a day. Failed tests keep a Playwright trace as a build artifact.
