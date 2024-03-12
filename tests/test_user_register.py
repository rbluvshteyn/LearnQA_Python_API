import string
import random
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime

class TestUserRegister(BaseCase):
    exclude_params = [
        "no_username",
        "no_password",
        "no_firstName",
        "no_lastName",
        "no_email"
    ]

    # Успешное создание пользователя
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response,200)
        Assertions.assert_json_has_key(response, "id")

    # Создание пользователя с существующим email
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content: {response.content}"

    # Создание пользователя с некорректным email (без @)
    def test_create_user_no_at(self):
        email = 'noatexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content: {response.content}"

    # Создание пользователя с коротким username длинной 1
    def test_create_user_short_name(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'username': 'a',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short",\
            f"Unexpected response content: {response.content}"

    # Создание пользователя с длинным username длинной > 250
    def test_create_user_long_name(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            'password': '123',
            'username': ''.join(random.choice(string.ascii_lowercase) for i in range(251)),
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long",\
            f"Unexpected response content: {response.content}"

    # Создание пользователя с отсутствующим полем
    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_no_param(self, condition):
        data = self.prepare_registration_data()

        if condition == "no_username":
            del data['username']
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The following required params are missed: username",\
                f"Unexpected response content: {response.content}"

        elif condition == "no_password":
            del data['password']
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The following required params are missed: password",\
                f"Unexpected response content: {response.content}"

        elif condition == "no_firstName":
            del data['firstName']
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The following required params are missed: firstName",\
                f"Unexpected response content: {response.content}"

        elif condition == "no_lastName":
            del data['lastName']
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The following required params are missed: lastName",\
                f"Unexpected response content: {response.content}"

        elif condition == "no_email":
            del data['email']
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The following required params are missed: email",\
                f"Unexpected response content: {response.content}"
