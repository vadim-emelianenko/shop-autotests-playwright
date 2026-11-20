import allure
import pytest

from data.users import new_user

pytestmark = [pytest.mark.api, allure.feature("API: accounts")]


@pytest.mark.smoke
def test_verify_login_with_valid_credentials(api, user):
    resp = api.verify_login(user["email"], user["password"])
    assert resp.code == 200
    assert resp.message == "User exists!"


def test_verify_login_with_wrong_password(api, user):
    resp = api.verify_login(user["email"], "wrong-password")
    assert resp.code == 404
    assert resp.message == "User not found!"


def test_verify_login_without_email_is_bad_request(api):
    resp = api.verify_login(None, "any")
    assert resp.code == 400


def test_delete_on_verify_login_is_not_allowed(api):
    assert api.delete_verify_login().code == 405


def test_user_details_match_registration_data(api, user):
    resp = api.user_by_email(user["email"])
    assert resp.code == 200
    details = resp.body["user"]
    assert details["email"] == user["email"]
    assert details["first_name"] == user["firstname"]
    assert details["last_name"] == user["lastname"]
    assert details["city"] == user["city"]


def test_duplicate_email_is_rejected(api, user):
    duplicate = new_user() | {"email": user["email"]}
    resp = api.create_account(duplicate)
    assert resp.code == 400
    assert resp.message == "Email already exists!"


def test_deleted_account_can_not_log_in(api):
    data = new_user()
    assert api.create_account(data).code == 201
    assert api.delete_account(data["email"], data["password"]).code == 200
    assert api.verify_login(data["email"], data["password"]).code == 404
