import pytest
import requests
from utils.helpers import generate_random_user
from tests.endpoints import REGISTER_URL, LOGIN_URL, USER_URL, INGREDIENTS_URL

@pytest.fixture(scope="session")
def api_client():
    return requests.Session()

@pytest.fixture(scope="function")
def generated_user_data():
    return generate_random_user()

@pytest.fixture(scope="function")
def registered_user(api_client, generated_user_data):
    # Регистрация нового пользователя
    response_register = api_client.post(REGISTER_URL, json=generated_user_data)
    assert response_register.status_code == 200  # Проверка успешной регистрации
    assert "accessToken" in response_register.json()  # Убедимся, что токен доступа присутствует в ответе
    generated_user_data["accessToken"] = response_register.json()["accessToken"]  # Сохраняем токен доступа
    return generated_user_data

@pytest.fixture(scope="function")
def logged_in_user(api_client, registered_user):
    # Вход зарегистрированного пользователя
    login_data = {"email": registered_user["email"], "password": registered_user["password"]}
    response_login = api_client.post(LOGIN_URL, json=login_data)
    assert response_login.status_code == 200  # Проверка успешного входа
    assert "accessToken" in response_login.json()  # Убедимся, что токен доступа присутствует в ответе
    return response_login.json()["accessToken"]

@pytest.fixture(scope="function")
def authenticated_user(logged_in_user):
    # Предоставление токена доступа
    return logged_in_user

@pytest.fixture(scope="function")
def cleanup_user(api_client, authenticated_user):
    # Удаление пользователя после завершения теста
    yield
    api_client.delete(USER_URL, headers={"Authorization": authenticated_user})

@pytest.fixture(scope="function")
def ingredients(api_client):
    response = api_client.get(INGREDIENTS_URL)
    return response.json().get("data", [])

@pytest.fixture(scope="function", params=["email", "password", "name"])
def missing_field(request):
    # Генерация случайных данных пользователя с отсутствующим полем
    user_data = generate_random_user()
    del user_data[request.param]
    return user_data, request.param
