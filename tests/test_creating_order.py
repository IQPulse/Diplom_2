import allure
from tests.endpoints import REGISTER_URL, LOGIN_URL, ORDERS_URL, USER_URL, INGREDIENTS_URL
from utils.helpers import generate_random_user


@allure.feature("Order Creation")
class TestOrderCreation:

    @allure.story("Create order with authentication")
    def test_create_order_with_authentication(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user credentials"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Get list of ingredients"):
            response_ingredients = api_client.get(INGREDIENTS_URL)
            ingredients = response_ingredients.json().get("data", [])

        with allure.step("Create an order"):
            order_data = {"ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]}  # Choose two ingredients
            response_order = api_client.post(ORDERS_URL, json=order_data, headers=headers)
            assert response_order.status_code == 200 and response_order.json().get("success") == True and \
                   response_order.json()["order"]["owner"]["email"] == user_data["email"]

        with allure.step("Delete the user"):
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.story("Create order without authentication")
    def test_create_order_without_authentication(self, api_client):
        with allure.step("Get list of ingredients"):
            response_ingredients = api_client.get(INGREDIENTS_URL)
            ingredients = response_ingredients.json().get("data", [])

        with allure.step("Create an order without authentication"):
            order_data = {"ingredients": [ingredients[0]["_id"]]}  # Choose the first ingredient
            response_order = api_client.post(ORDERS_URL, json=order_data)

        with allure.step("Check absence of 'email' field in response"):
            assert "email" not in response_order.json().get("order", {})

    @allure.story("Create order with specified ingredients")
    def test_create_order_with_order_ingredients(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user credentials"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Get list of ingredients"):
            response_ingredients = api_client.get(INGREDIENTS_URL)
            ingredients = response_ingredients.json().get("data", [])

        with allure.step("Create an order"):
            order_data = {"ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]}  # Choose two ingredients
            response_order = api_client.post(ORDERS_URL, json=order_data, headers=headers)
            assert response_order.json().get("order", {}).get("ingredients", [])[0]["_id"] == ingredients[0]["_id"] and \
                   response_order.json().get("order", {}).get("ingredients", [])[1]["_id"] == ingredients[1]["_id"]

        with allure.step("Delete the user"):
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.story("Create order with no ingredients")
    def test_create_order_no_ingredients(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user credentials"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Send request to create order without specifying ingredients"):
            response_order = api_client.post(ORDERS_URL, json={}, headers=headers)
            assert response_order.status_code == 400 and response_order.json().get(
                "success") == False and response_order.json().get("message") == "Ingredient ids must be provided"

        with allure.step("Delete the user"):
            response_delete = api_client.delete(USER_URL, headers=headers)

    @allure.story("Create order with invalid ingredients hash")
    def test_create_order_invalid_ingredients_hash(self, api_client):
        with allure.step("Create a new user"):
            user_data = generate_random_user()
            response_register = api_client.post(REGISTER_URL, json=user_data)

        with allure.step("Login with created user credentials"):
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            response_login = api_client.post(LOGIN_URL, json=login_data)
            access_token = response_login.json().get("accessToken")
            headers = {"Authorization": access_token}

        with allure.step("Get list of ingredients"):
            response_ingredients = api_client.get(INGREDIENTS_URL, headers=headers)
            ingredients = response_ingredients.json().get("data", [])

        with allure.step("Create an order with invalid ingredients hash"):
            ingredients_ids = [ingredient["_id"] for ingredient in ingredients]
            invalid_ingredients = ingredients_ids + ["1000"]
