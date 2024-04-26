import allure
from tests.endpoints import REGISTER_URL, LOGIN_URL, USER_URL
from utils.helpers import generate_random_user


@allure.feature("User Login")
class TestUserLogin:

    @allure.story("Login with existing user credentials")
    def test_login_existing_user(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user credentials"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response = api_client.post(LOGIN_URL, json=login_data)
            assert response.status_code == 200 and response.json().get("success") == True

        with allure.step("Delete the user"):
            access_token = response.json().get("accessToken")
            headers = {"Authorization": access_token}
            response = api_client.delete(USER_URL, headers=headers)

    @allure.story("Login with wrong credentials")
    def test_login_wrong_credentials(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with incorrect credentials"):
            login_data = {"email": user_data["email"], "password": user_data["password"] + "1000"}
            response = api_client.post(LOGIN_URL, json=login_data)
            assert response.status_code == 401 and response.json().get("success") == False and response.json().get(
                "message") == "email or password are incorrect"

        with allure.step("Delete the user"):
            access_token = response.json().get("accessToken")
            headers = {"Authorization": access_token}
            response = api_client.delete(USER_URL, headers=headers)
