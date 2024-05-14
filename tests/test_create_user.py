import allure
from tests.endpoints import REGISTER_URL, USER_URL

@allure.feature("User Registration")
class TestUserRegistration:

    @allure.title("Create user")
    def test_create_user(self, api_client, registered_user):
        with allure.step("Delete the user"):
            user_data = registered_user
            access_token = user_data["accessToken"]
            headers = {"Authorization": access_token}
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.title("Create existing user")
    def test_create_existing_user(self, api_client, registered_user):
        user_data = registered_user
        with allure.step("Attempt to create user with existing credentials"):
            response = api_client.post(REGISTER_URL, json=user_data)
            assert response.status_code == 403 and response.json().get("success") == False and response.json().get(
                "message") == "User already exists"
        with allure.step("Delete the user"):
            access_token = user_data["accessToken"]
            headers = {"Authorization": access_token}
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.title("Create user with missing field")
    def test_create_user_missing_field(self, api_client, missing_field):
        user_data, missing_param = missing_field
        with allure.step(f"Create a new user with missing field: {missing_param}"):
            response = api_client.post(REGISTER_URL, json=user_data)
            assert response.status_code == 403 and response.json().get("success") == False and response.json().get(
                "message") == "Email, password and name are required fields"
