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

Test users are created through the API, so UI tests skip the signup form. Expected values come from the API where possible.

Ad and consent hosts are blocked, their popups cover buttons on the demo site.

The API answers HTTP 200 to everything and puts the real status into `responseCode`, so tests check that field.

CI runs lint and tests on push to main, on pull requests and once a day. A failed test leaves a Playwright trace in `test-results` locally and as a build artifact in CI.
