from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime

class TestUserEdit(BaseCase):
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
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_no_login(self):
        response1 = MyRequests.post("/user/", data=self.data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        id_user = response1.json()["id"]

        new_name = "Changed name"

        response2 = MyRequests.put(f"/user/{id_user}", data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        assert "Auth token not supplied" in response2.text, "Error! Successful edit by unauthorised user!"

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_by_another_user(self):
        # Создаем 2 юзера
        response1 = MyRequests.post("/user/", data=self.data1)
        response2 = MyRequests.post("/user/", data=self.data2)

        # Логин user1
        response3 = MyRequests.post("/user/login", data=self.cred1)

        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")
        user_id1 = self.get_json_value(response3, "user_id")

        # Логин user2
        response4 = MyRequests.post("/user/login", data=self.cred2)

        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")
        user_id2 = self.get_json_value(response4, "user_id")

        # Пытаемся изменить имя user2 будучи авторизованным user1
        new_email = f"new{self.random_part}@mail.ru"

        response5 = MyRequests.put(
            f"/user/{user_id2}",  # id user2
            data={"email": new_email},
            headers={"x-csrf-token": token1},  # token user 1
            cookies={"auth_sid": auth_sid1}  # auth_sid1 user1
        )

        # Проверяем изменилось ли Имя у второго пользователя
        response6 = MyRequests.get(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2}
        )

        Assertions.assert_json_value_by_name(
            response6,
            "email",
            self.data2["email"],
            "Wrong email of the user after edit"
        )

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_noat_email(self):
        # Регистрация
        response = MyRequests.post("/user/", data=self.data1)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        # Логин
        response2 = MyRequests.post("/user/login", data=self.cred1)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        new_email = f"new{self.random_part}mail.ru"

        # Пробуем поменять email на неправильный
        response3 = MyRequests.put(
            f"/user/{user_id}",
            data={"email": new_email},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Првоерка невозможности замены email на email без @
        Assertions.assert_code_status(response3,400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Invalid email format",
            "Wrong email of the user after edit"
        )

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_short_firstname(self):
        # Регистрация
        response = MyRequests.post("/user/", data=self.data1)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        # Логин
        response2 = MyRequests.post("/user/login", data=self.cred1)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        new_short_name = 'a'

        # Пробуем поменять firstName на неправильный
        response3 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_short_name},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Првоерка невозможности замены firstName на короткий
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "The value for field `firstName` is too short",
            "Wrong firstName of the user after edit"
        )