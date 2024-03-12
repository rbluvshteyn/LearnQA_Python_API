from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime

class TestUserGet(BaseCase):
    # Получение данных неавторизованным пользователем
    def test_get_user_detail_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response,"username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    # Получение данных пользователем о себе
    def test_get_user_detail_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    # Получение одним пользователем данных другого пользователя
    def test_get_user_detail_from_other_user(self):
        # Создаем 2 юзера, проверяем что все ок
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")

        data_user1 = self.prepare_registration_data()
        data_user2 = self.prepare_registration_data(f"{random_part}@mail.ru")

        response1 = MyRequests.post("/user/", data=data_user1)
        response2 = MyRequests.post("/user/", data=data_user2)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        # Креды для логина
        cred_user1 = {
            'email': data_user1["email"],
            'password': data_user1["password"]
        }

        cred_user2 = {
            'email': data_user2["email"],
            'password': data_user2["password"]
        }

        # Логинимся двумя юзерами
        response3 = MyRequests.post("/user/login", data=cred_user1)
        response4 = MyRequests.post("/user/login", data=cred_user2)

        user_id_from_auth_method1 = self.get_json_value(response3, "user_id")

        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        # Запрос на id первого юзера, токен и auth_sid от второго юзера
        response5 = MyRequests.get(
            f"/user/{user_id_from_auth_method1}",
            headers={"x-csrf-token": f"{token2}"},
            cookies={"auth_sid": f"{auth_sid2}"}
        )

        Assertions.assert_json_has_not_key(response2, "username")
        print(response5.text)