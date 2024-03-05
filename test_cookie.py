import requests

class TestCookie:
    def test_cookie_method(self):
        url_cookie = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url_cookie)

        print(response.cookies.get_dict())

        assert "HomeWork" in response.cookies, "No cookie \"HomeWork\" in response!!"
        assert "hw_value" == response.cookies.get("HomeWork"), "Cookie is not correct!"