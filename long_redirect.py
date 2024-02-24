import requests

long_redirect_url = "https://playground.learnqa.ru/api/long_redirect"

response = requests.get(long_redirect_url, allow_redirects=True)

redirect_number = len(response.history)
last_url = response.history[-1].url

print(f'Количестов редиректов в запросе: {redirect_number}')
print(f'Итоговый URL: {last_url}')
