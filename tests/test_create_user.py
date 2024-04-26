import allure
from tests.endpoints import REGISTER_URL, USER_URL
from utils.helpers import generate_random_user


@allure.feature("User Registration")
class TestUserRegistration:

    @allure.story("Create user")
    def test_create_user(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response = api_client.post(REGISTER_URL, json=user_data)
            assert response.status_code == 200 and response.json().get("success") == True

        with allure.step("Delete the user"):
            access_token = response.json().get("accessToken")
            headers = {"Authorization": access_token}
            response = api_client.delete(USER_URL, headers=headers)

    @allure.story("Create existing user")
    def test_create_existing_user(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Attempt to create user with existing credentials"):
            response = api_client.post(REGISTER_URL, json=user_data)
            assert response.status_code == 403 and response.json().get("success") == False and response.json().get(
                "message") == "User already exists"

        with allure.step("Delete the user"):
            access_token = response.json().get("accessToken")
            headers = {"Authorization": access_token}
            response = api_client.delete(USER_URL, headers=headers)

    @allure.story("Create user with missing field")
    def test_create_user_missing_field(self, api_client):
        with allure.step("Create a new user with missing field"):
            user_data = generate_random_user()
            del user_data["email"]
            response = api_client.post(REGISTER_URL, json=user_data)
            assert response.status_code == 403 and response.json().get("success") == False and response.json().get(
                "message") == "Email, password and name are required fields"
