import allure
from tests.endpoints import REGISTER_URL, LOGIN_URL, ORDERS_URL

@allure.feature("Orders")
class TestOrderSpecificUser:

    @allure.title("Get orders for authenticated user")
    def test_get_orders_authenticated_user(self, api_client, cleanup_user, generated_user_data):
        with allure.step("Create a new user"):
            response_register = api_client.post(REGISTER_URL, json=generated_user_data)

        with allure.step("Login as the created user"):
            login_data = {"email": generated_user_data["email"], "password": generated_user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Get orders for the authenticated user"):
            response_orders = api_client.get(ORDERS_URL, headers=headers)
            assert response_orders.status_code == 200 and response_orders.json().get("success") == True

    @allure.title("Create order for unauthorized user")
    def test_create_order_unauthorized_user(self, api_client):
        with allure.step("Send a request to create an order without authorization"):
            response = api_client.post(ORDERS_URL, json={})
            assert response.status_code == 400 and response.json().get("success") == False and response.json().get(
                "message") == "Ingredient ids must be provided"
