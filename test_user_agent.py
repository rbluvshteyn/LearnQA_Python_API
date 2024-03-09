import requests
import pytest

class TestUserAgent:
    user_agent = [
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    ]

    @pytest.mark.parametrize("user_agent", user_agent)
    def test_user_agent(self, user_agent):
        url_user_agent = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        response = requests.get(url_user_agent, headers={"User-Agent":user_agent})
        dict_response = response.json()

        if user_agent == "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30":
            platform = "Mobile"
            browser = "No"
            device = "Android"
        elif user_agent == "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1":
            platform = "Mobile"
            browser = "Chrome"
            device = "iOS"
        elif user_agent == "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)":
            platform = "Googlebot"
            browser = "Unknown"
            device = "Unknown"
        elif user_agent == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0":
            platform = "Web"
            browser = "Chrome"
            device = "No"
        elif user_agent == "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1":
            platform = "Mobile"
            browser = "No"
            device = "iPhone"

        assert platform == dict_response["platform"], f"Wrong platform value:\"{dict_response['platform']}\" for user-agent:{user_agent}"
        assert browser == dict_response["browser"], f"Wrong browser value:\"{dict_response['browser']}\" for user-agent:{user_agent}"
        assert device == dict_response["device"], f"Wrong device value:\"{dict_response['device']}\" for user-agent:{user_agent}"