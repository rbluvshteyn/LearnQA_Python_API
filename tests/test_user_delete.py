from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime
import allure

@allure.epic("Delete cases")
class TestUserDelete(BaseCase):
    def setup_method(self):
        self.random_part = datetime.now().strftime("%m%d%Y%H%M%S")

        self.data1 = self.prepare_registration_data()
        self.data2 = self.prepare_registration_data(f"{self.random_part}@mail.ru")

        self.cred1 = {
            'email': self.data1["email"],
            'password': self.data1["password"]
        }

        self.cred2 = {
            'email': self.data2["email"],
            'password': self.data2["password"]
        }

    @allure.description("Тест на попытку удалить пользователя c id=2")
    # Тест на попытку удалить пользователя id=2
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Логин пользователем vinkotov@example.com"):
            response = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response, "auth_sid")
            token = self.get_header(response, "x-csrf-token")
            user_id = self.get_json_value(response, "user_id")

        with allure.step("Попытка удалить пользователя vinkotov@example.com"):
            response2 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response2, 400)
            Assertions.assert_json_value_by_name(
                response2,
                "error",
                "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                "Wrong response delete user"
            )

    @allure.description("Позитивный тест удаления пользователя")
    # Позитивный тест удаления пользователя
    def test_delete_user(self):
        # Регистрация
        with allure.step("Регистрация пользователя"):
            self.data = self.prepare_registration_data()

            response = MyRequests.post("/user/", data=self.data)

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

            data = {
                "email": self.data["email"],
                "password": self.data["password"]
            }

        # Логин
        with allure.step("Логин"):
            response2 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            user_id = self.get_json_value(response2, "user_id")

        # Удаление
        with allure.step("Удаление"):
            response3 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_code_status(response3, 200)

            response4 = MyRequests.get(f"/user/{user_id}")

            Assertions.assert_code_status(response4, 404)
            assert response4.text == "User not found", "Wrong response delete user"

    @allure.description("Тест на попытку удаления пользователя, будучи авторизованными другим пользователем.")
    # попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_by_another_user(self):
        # Создаем 2 юзера
        with allure.step("Регистрация 2х пользователей"):
            response1 = MyRequests.post("/user/", data=self.data1)
            response2 = MyRequests.post("/user/", data=self.data2)

        # Логин user1
        with allure.step("Логин user1"):
            response3 = MyRequests.post("/user/login", data=self.cred1)

            auth_sid1 = self.get_cookie(response3, "auth_sid")
            token1 = self.get_header(response3, "x-csrf-token")
            user_id1 = self.get_json_value(response3, "user_id")

        # Логин user2
        with allure.step("Логин user2"):
            response4 = MyRequests.post("/user/login", data=self.cred2)

            auth_sid2 = self.get_cookie(response4, "auth_sid")
            token2 = self.get_header(response4, "x-csrf-token")
            user_id2 = self.get_json_value(response4, "user_id")

        # Пытаемся удалить user1 будучи авторизованным user2
        with allure.step("Попытка удалить user1 из под user2"):
            response5 = MyRequests.delete(
                f"/user/{user_id1}",  # # id user1
                headers={"x-csrf-token": token2},  # # token user1
                cookies={"auth_sid": auth_sid2}  # # auth_sid user1
            )

            # Проверяем удаление
            response6 = MyRequests.get(
                f"/user/{user_id1}",
                headers={"x-csrf-token": token1},
                cookies={"auth_sid": auth_sid1}
            )

            expected_fields = ["id", "username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response6, expected_fields)