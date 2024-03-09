import time
import requests
import json

longtime_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

#1 Создаем задачу
create_task = requests.get(longtime_url)
create_task_json = json.loads(create_task.text)

#2 Делаем запрос до готовности задачи, проверяем поле status
check_status = requests.get(longtime_url, params=f'token={create_task_json["token"]}')
check_status_json = json.loads(check_status.text)

if 'status' in check_status_json and check_status_json['status'] == "Job is NOT ready":
    print(f'Задача еще не готова! Ждем {create_task_json["seconds"]} секунд.')

    #3 Ждем нужное время, если status правильный
    time.sleep(create_task_json['seconds'])

    #4 Делаем запрос после готовности задачи, проверяем status и result
    check_result = requests.get(longtime_url, params=f'token={create_task_json["token"]}')
    check_result_json = json.loads(check_result.text)

    if check_result_json['status'] == "Job is ready" and 'result' in check_result_json:
        print(f'Задача ГОТОВА! Результат {check_result_json["result"]}')
    else:
        raise ValueError(f'Ошибка:{check_result_json["status"]}')
else:
    raise ValueError(f'Ошибка:{check_status_json["error"]}')