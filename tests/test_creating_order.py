import allure
from tests.endpoints import ORDERS_URL

@allure.feature("Order Creation")
class TestOrderCreation:

    @allure.title("Create order with authentication")
    def test_create_order_with_authentication(self, api_client, registered_user, ingredients):
        access_token = registered_user["accessToken"]
        headers = {"Authorization": access_token}

        order_data = {"ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]}
        response_order = api_client.post(ORDERS_URL, json=order_data, headers=headers)
        assert response_order.status_code == 200 and response_order.json().get("success") == True and \
               response_order.json()["order"]["owner"]["email"] == registered_user["email"]

    @allure.title("Create order without authentication")
    def test_create_order_without_authentication(self, api_client, ingredients):
        order_data = {"ingredients": [ingredients[0]["_id"]]}
        response_order = api_client.post(ORDERS_URL, json=order_data)
        assert "email" not in response_order.json().get("order", {})

    @allure.title("Create order with specified ingredients")
    def test_create_order_with_order_ingredients(self, api_client, registered_user, ingredients):
        access_token = registered_user["accessToken"]
        headers = {"Authorization": access_token}

        order_data = {"ingredients": [ingredients[0]["_id"], ingredients[1]["_id"]]}
        response_order = api_client.post(ORDERS_URL, json=order_data, headers=headers)
        assert response_order.json().get("order", {}).get("ingredients", [])[0]["_id"] == ingredients[0]["_id"] and \
               response_order.json().get("order", {}).get("ingredients", [])[1]["_id"] == ingredients[1]["_id"]

    @allure.title("Create order with no ingredients")
    def test_create_order_no_ingredients(self, api_client, registered_user):
        access_token = registered_user["accessToken"]
        headers = {"Authorization": access_token}

        response_order = api_client.post(ORDERS_URL, json={}, headers=headers)
        assert response_order.status_code == 400 and response_order.json().get(
            "success") == False and response_order.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Create order with invalid ingredients hash")
    def test_create_order_invalid_ingredients_hash(self, api_client, registered_user, ingredients):
        access_token = registered_user["accessToken"]
        headers = {"Authorization": access_token}

        ingredients_ids = [ingredient["_id"] for ingredient in ingredients]
        invalid_ingredients = ingredients_ids + ["1000"]
