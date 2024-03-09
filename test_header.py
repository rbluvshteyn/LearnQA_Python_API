import requests

class TestHeader:
    def test_header(self):
        dict_head = {
            'Date': 'Sat, 09 Mar 2024 15:36:30 GMT',
            'Content-Type': 'application/json',
            'Content-Length': '15',
            'Connection': 'keep-alive',
            'Keep-Alive': 'timeout=10',
            'Server': 'Apache',
            'x-secret-homework-header': 'Some secret value',
            'Cache-Control': 'max-age=0',
            'Expires': 'Sat, 09 Mar 2024 15:36:30 GMT'
        }

        url_header = "https://playground.learnqa.ru/api/homework_header"

        response = requests.get(url_header)
        print(response.headers)

        for key in dict_head:
            assert key in response.headers, f"No key {key} in response!"
            if key != "Date" and key != "Expires":  # скипаем заголовки Date и Expires, т.к. они не имеют фиксированного значения
                assert dict_head[key] == response.headers[key], f"Wrong value of header {key} in response!"