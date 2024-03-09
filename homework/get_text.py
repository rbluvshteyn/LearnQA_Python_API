import requests

get_text_url = "https://playground.learnqa.ru/api/get_text"

response = requests.get(get_text_url)
print(response.text)