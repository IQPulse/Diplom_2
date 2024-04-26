import allure
from tests.endpoints import REGISTER_URL, LOGIN_URL, USER_URL
from utils.helpers import generate_random_user


@allure.feature("Changing User Data")
class TestChangingUserData:

    @allure.story("Update user email")
    def test_update_user_email(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Update user email"):
            updated_email = user_data["email"] + "1000"
            updated_data = {"email": updated_email, "name": user_data["name"]}
            response_update = api_client.patch(USER_URL, json=updated_data, headers=headers)
            assert response_update.status_code == 200 and response_update.json().get("success") == True

        with allure.step("Delete the user"):
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.story("Update user name")
    def test_update_user_name(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Update user name"):
            updated_name = user_data["name"] + "1000"
            updated_data = {"email": user_data["email"], "name": updated_name}
            response_update = api_client.patch(USER_URL, json=updated_data, headers=headers)
            assert response_update.status_code == 200 and response_update.json().get("success") == True

        with allure.step("Delete the user"):
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.story("Update user email unauthorized")
    def test_update_user_email_unauthorized(self, api_client):
        with allure.step("Generate random user data"):
            user_data = generate_random_user()
            user_data["email"] += "1000"  # Add "1000" to email

        with allure.step("Attempt to update user email without authorization"):
            response = api_client.patch(USER_URL, json=user_data)
            assert response.status_code == 401 and response.json().get("success") == False and response.json().get(
                "message") == "You should be authorised"

    @allure.story("Update user password unauthorized")
    def test_update_user_password_unauthorized(self, api_client):
        with allure.step("Generate random user data"):
            user_data = generate_random_user()
            user_data["password"] += "1000"  # Add "1000" to password

        with allure.step("Attempt to update user password without authorization"):
            response = api_client.patch(USER_URL, json=user_data)
            assert response.status_code == 401 and response.json().get("success") == False and response.json().get(
                "message") == "You should be authorised"
