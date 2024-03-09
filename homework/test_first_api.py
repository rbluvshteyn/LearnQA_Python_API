import requests
import pytest

class TestFirstAPI:
    names = [
        ("Roman"),
        ("Vilaly"),
        ("")
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        name = "Roman"
        data = {'name':name}

        response = requests.get(url, params=data)
        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        assert "answer" in response_dict, "No field 'answer' in response!"

        if len(name) == 0:
            expect_response_text = "Hello, someone"
        else:
            expect_response_text = f"Hello, {name}"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expect_response_text, "Actual text in response NOT correct!"