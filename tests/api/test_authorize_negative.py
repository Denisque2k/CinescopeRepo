import pytest
import requests
from constants import BASE_URL, HEADERS, LOGIN_ENDPOINT

class TestAuthorizeNegativeAPI:
    def test_authorize_negative_user(self, auth_session_login_negative, test_user):
        login_data = auth_session_login_negative["login_data"]
        user = auth_session_login_negative["user"]


        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

        response = requests.post(login_url, json=login_data, headers=HEADERS)

        print(f"Response status: {response.status_code}")
        print(f"Account data: {test_user}")
        print(f"Response body: {response.json()}")
        response_data = response.json()
        assert response.status_code == 200, "Ошибка авторизации, неверный email/пароль"
        assert "accessToken" in response_data, "Токен авторизации не был передан"
        assert response_data["user"]["email"] == test_user["email"], "Email не совпадает"