import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase, Assertions):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        self.url_login = "https://playground.learnqa.ru/api/user/login"
        self.url_auth = "https://playground.learnqa.ru/api/user/auth"
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post(self.url_login, data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth = self.get_json_value(response1, "user_id")

    def test_user_auth(self):
        response2 = requests.get(
            self.url_auth,
            headers={"x-csrf-token":self.token},
            cookies={"auth_sid":self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth,
            "User id from auth method is NOT equal to user id from check method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(
                self.url_auth,
                headers={"x-csrf-token":self.token}
            )
        else:
            response2 = requests.get(
                self.url_auth,
                cookies={"auth_sid":self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )