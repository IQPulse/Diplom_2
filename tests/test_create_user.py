import pytest
import requests
from utils.helpers import generate_random_user

class TestUserRegistration:

    def test_create_user(self, api_client):
        user_data = generate_random_user()
        response = api_client.post("https://stellarburgers.nomoreparties.site/api/auth/register", json=user_data)
        assert response.status_code == 200 and response.json().get("success") == True
        # Удаление пользователя
        access_token = response.json().get("accessToken")
        headers = {"Authorization": access_token}
        response = api_client.delete("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers)

    def test_create_existing_user(self, api_client):
        user_data = generate_random_user()
        response = api_client.post("https://stellarburgers.nomoreparties.site/api/auth/register", json=user_data)
        response = api_client.post("https://stellarburgers.nomoreparties.site/api/auth/register", json=user_data)
        assert response.status_code == 403 and response.json().get("success") == False and response.json().get("message") == "User already exists"
        # Удаление пользователя
        access_token = response.json().get("accessToken")
        headers = {"Authorization": access_token}
        response = api_client.delete("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers)

    def test_create_user_missing_field(self, api_client):
        user_data = generate_random_user()
        # Удаление имени пользователя, чтобы создать запрос с пропущенным обязательным полем
        del user_data["email"]
        response = api_client.post("https://stellarburgers.nomoreparties.site/api/auth/register", json=user_data)
        assert response.status_code == 403 and response.json().get("success") == False and response.json().get("message") == "Email, password and name are required fields"