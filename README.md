# shop-autotests-playwright

UI and API autotests for [Automation Exercise](https://automationexercise.com), a public demo shop.
Python, Playwright, pytest, requests, Docker, GitHub Actions, Allure.

[![tests](https://github.com/vadim-emelianenko/shop-autotests-playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/vadim-emelianenko/shop-autotests-playwright/actions/workflows/tests.yml)
Allure report: https://vadim-emelianenko.github.io/shop-autotests-playwright/

## Run

```bash
make test
```

Needs only Docker. Without Docker:

```bash
pip install -r requirements.txt && playwright install chromium && pytest
```

`pytest -m smoke` runs the short critical subset, `pytest -m api` runs API tests only.

## What is covered

| Area | Checks |
|---|---|
| API catalog | product and brand lists, search by name and category, wrong HTTP methods, missing parameters |
| API accounts | create, login check, user details, duplicate email, deleted user can not log in |
| UI auth | login with a user created through the API, wrong password, logout, signup with a taken email |
| UI catalog | UI and API show the same products, search, empty search, product card vs API data |
| UI cart | add, sum of quantities, price x quantity, remove, cart kept after login |

## How it is built

```
api/client.py      thin requests wrapper, every call is an Allure step
pages/             Page Objects, locators live only here
data/users.py      unique test users from Faker
conftest.py        fixtures: API client, user created by API and deleted after the test,
                   page with ad and consent scripts blocked, screenshot on failure
tests/api, tests/ui
```

A few decisions worth explaining:

- Test users are created through the API, not through the UI form. UI tests spend time only on what they check, and every user is removed in teardown.
- Many UI tests compare the page with the API response instead of hardcoded values, so they keep working when the shop changes its catalog.
- The demo site shows full screen ads at random. Requests to ad and consent hosts are aborted in the `page` fixture, otherwise they cover buttons and break clicks.
- The API always answers HTTP 200 and puts the real status into `responseCode`. The client exposes both, tests check the body code.
- CI runs on every push and once a day, the report is published to GitHub Pages.

## Found while writing tests

To be filled after the first CI runs, only with what really reproduced.
