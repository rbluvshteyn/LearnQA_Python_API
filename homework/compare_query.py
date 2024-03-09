import requests

compare_query_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

#1. Делает http-запрос любого типа без параметра method
response_get = requests.get(compare_query_url)

print("Запрос любого типа без параметра:")
print(response_get.status_code)
print(response_get.text)

#2. Делает http-запрос не из списка. Например, HEAD
response_head = requests.head(compare_query_url, data='method=HEAD')

print("\nЗапрос не из списка(HEAD)")
print(response_head.status_code)
print(response_head.text)

#3. Делает запрос с правильным значением method
response_post = requests.delete(compare_query_url, data='method=DELETE')

print("\nЗапрос с правильным параметром")
print(response_post.status_code)
print(response_post.text)

#4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method
methods = ['GET', 'POST', 'PUT', 'DELETE']

for method in methods:
    for param in methods:
        # Проверяем метод GET
        if method == 'GET':
            # Совпадающие тип запроса и параметр
            if method == param:
                response_method = requests.request(method, compare_query_url, params=f'method={param}')
                if response_method.text != '{"success":"!"}':
                    print("\nТип запроса и параметр method СОВПАДАЮТ, сервер отвечает НЕКОРРЕКТНО!")
                    print(f"{method}, параметр {param}")
                    print(response_method.text)
            # НЕСовпадающие тип запроса и параметр
            else:
                response_method = requests.request(method, compare_query_url, params=f'method={param}')
                if response_method.text == '{"success":"!"}':
                    print("\nТип запроса и параметр method НЕ СОВПАДАЮТ, сервер отвечает НЕКОРРЕКТНО!")
                    print(f"{method}, параметр {param}")
                    print(response_method.text)
        # Проверяем методы 'POST', 'PUT', 'DELETE'
        else:
            # Совпадающие тип запроса и параметр
            if method == param:
                response_method = requests.request(method, compare_query_url, data=f'method={param}')
                if response_method.text != '{"success":"!"}':
                    print("\nТип запроса и параметр method СОВПАДАЮТ, сервер отвечает НЕКОРРЕКТНО!")
                    print(f"{method}, параметр {param}")
                    print(response_method.text)
            # НЕСовпадающие тип запроса и параметр
            else:
                response_method = requests.request(method, compare_query_url, data=f'method={param}')
                if response_method.text == '{"success":"!"}':
                    print("\nТип запроса и параметр method НЕ СОВПАДАЮТ, сервер отвечает НЕКОРРЕКТНО!")
                    print(f"{method}, параметр {param}")
                    print(response_method.text)