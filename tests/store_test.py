import allure
import httpx

from util.logging_config import logger


@allure.title("Test for place a new order successfully")
@allure.description(
    "This test verifies that a new order can be placed with valid data."
)
def test_place_order_success(base_url):
    logger.info("Running test: test_place_order_success")
    order_data = {
        "pet_id": 1,
        "quantity": 2,
        "shipDate": "2024-12-23T10:00:00Z",
        "status": "placed",
        "complete": True,
    }
    logger.debug(f"Placing order with data: {order_data}")
    response = httpx.post(f"{base_url}/store/order", json=order_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data["pet_id"] == 1
    assert response_data["status"] == "placed"
    logger.info("Test passed: test_place_order_success")


@allure.title("Test for getting order by ID")
@allure.description(
    "This test retrieves an existing order by ID and checks data is correct."
)
def test_get_order_by_id_success(base_url):
    logger.info("Running test: test_get_order_by_id_success")
    order_id = 1
    logger.debug(f"Getting order by ID: {order_id}")
    response = httpx.get(f"{base_url}/store/order/{order_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data["id"] == order_id
    assert response_data["status"] == "placed"
    logger.info("Test passed: test_get_order_by_id_success")


@allure.title("Test for getting non-existent order")
@allure.description(
    "This test ensures that it's not possible to get an order by a non-existent ID."
)
def test_get_nonexistent_order(base_url):
    logger.info("Running test: test_get_nonexistent_order")
    non_existent_order_id = 999
    logger.debug(f"Getting order by non-existent ID: {non_existent_order_id}")
    response = httpx.get(f"{base_url}/store/order/{non_existent_order_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data["detail"] == "Order not found"
    logger.info("Test passed: test_get_non_existed_order")


@allure.title("Test for deleting order from data")
@allure.description(
    "This test deletes an existing order and verifies it is no longer accessible afterwards."
)
def test_delete_order_success(base_url):
    logger.info("Running test: test_delete_order_success")
    order_id = 1
    logger.debug(f"Deleting order with ID: {order_id}")
    response = httpx.delete(f"{base_url}/store/order/{order_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data["message"] == f"Order with ID {order_id} has been deleted"
    logger.info(f"Order with ID {order_id} deleted successfully")

    response = httpx.get(f"{base_url}/store/order/{order_id}")
    logger.debug(f"Checking if order with ID {order_id} still exists")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    logger.info("Test passed: test_delete_order_success")


@allure.title("Test for getting store inventory")
@allure.description(
    "This test fetches the store inventory and validates the presence of expected statuses."
)
def test_get_inventory_success(base_url):
    logger.info("Running test: test_get_inventory_success")
    response = httpx.get(f"{base_url}/store/inventory")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    inventory = response.json()
    assert isinstance(inventory, dict), "Response must be a dictionary"

    assert "pending" in inventory, "Inventory should contain 'pending' status"
    assert "sold" in inventory, "Inventory should contain 'sold' status"

    assert inventory["pending"] == 1, "Incorrect count for 'pending' status"
    assert inventory["sold"] == 1, "Incorrect count for 'sold' status"
    logger.info("Test passed: test_get_inventory_success")
