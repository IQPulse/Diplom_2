import allure
from tests.endpoints import REGISTER_URL, LOGIN_URL

@allure.feature("User Login")
class TestUserLogin:

    @allure.title("Login with existing user credentials")
    def test_login_existing_user(self, api_client, cleanup_user, generated_user_data):
        with allure.step("Create a new user"):
            response_register = api_client.post(REGISTER_URL, json=generated_user_data)

        with allure.step("Login with created user credentials"):
            login_data = {"email": generated_user_data["email"], "password": generated_user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            assert response_login.status_code == 200 and response_login.json().get("success") == True

    @allure.title("Login with wrong credentials")
    def test_login_wrong_credentials(self, api_client, cleanup_user, generated_user_data):
        with allure.step("Create a new user"):
            response_register = api_client.post(REGISTER_URL, json=generated_user_data)

        with allure.step("Login with incorrect credentials"):
            login_data = {"email": generated_user_data["email"], "password": generated_user_data["password"] + "1000"}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            assert response_login.status_code == 401 and response_login.json().get("success") == False and response_login.json().get(
                "message") == "email or password are incorrect"