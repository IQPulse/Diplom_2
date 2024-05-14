import allure
from tests.endpoints import  USER_URL

@allure.feature("Changing User Data")
class TestChangingUserData:

    @allure.title("Test Update User Email")
    def test_update_user_email(self, api_client, registered_user, authenticated_user, cleanup_user):
        access_token = authenticated_user
        user_data = registered_user

        updated_email = user_data["email"] + "1000"
        updated_data = {"email": updated_email, "name": user_data["name"]}
        response_update = api_client.patch(USER_URL, json=updated_data, headers={"Authorization": access_token})
        assert response_update.status_code == 200 and response_update.json().get("success") == True

    @allure.title("Test Update User Name")
    def test_update_user_name(self, api_client, registered_user, authenticated_user, cleanup_user):
        access_token = authenticated_user
        user_data = registered_user

        updated_name = user_data["name"] + "1000"
        updated_data = {"email": user_data["email"], "name": updated_name}
        response_update = api_client.patch(USER_URL, json=updated_data, headers={"Authorization": access_token})
        assert response_update.status_code == 200 and response_update.json().get("success") == True

    @allure.title("Test Update User Email Unauthorized")
    def test_update_user_email_unauthorized(self, api_client, generated_user_data):
        response = api_client.patch(USER_URL, json=generated_user_data)
        assert response.status_code == 401 and response.json().get("success") == False and response.json().get(
            "message") == "You should be authorised"

    @allure.title("Test Update User Password Unauthorized")
    def test_update_user_password_unauthorized(self, api_client, generated_user_data):
        response = api_client.patch(USER_URL, json=generated_user_data)
        assert response.status_code == 401 and response.json().get("success") == False and response.json().get(
            "message") == "You should be authorised"
