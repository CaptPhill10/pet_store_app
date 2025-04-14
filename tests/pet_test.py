import allure
import httpx
import pytest

from util.logging_config import logger


@allure.title("Test to get a pet by ID (successful)")
@allure.description("This test ensures that it's possible to get a pet by ID.")
def test_get_pet_by_id_success(base_url):
    pet_id = 1
    logger.info(f"Running test: test_get_pet_by_id_success with pet_id: {pet_id}")
    response = httpx.get(f"{base_url}/pet/{pet_id}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    pet_data = response.json()
    assert pet_data["id"] == pet_id
    assert pet_data["name"] == "Buddy"
    assert pet_data["category"]["name"] == "Dogs"
    assert pet_data["status"] == "available"
    logger.info(f"Test passed: test_get_pet_by_id_success with pet_id: {pet_id}")


@allure.title("Test to get a pet by ID (unsuccessful)")
@allure.description(
    "This test ensures that it's not possible to get a pet by wrong ID."
)
def test_get_pet_by_id_not_found(base_url):
    pet_id = 999
    logger.info(f"Running test: test_get_pet_by_id_not_found with pet_id: {pet_id}")
    response = httpx.get(f"{base_url}/pet/{pet_id}")
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    error_data = response.json()
    assert error_data["detail"] == "Pet not found"
    logger.info(f"Test passed: test_get_pet_by_id_not_found with pet_id: {pet_id}")


@allure.title("Test to get a pet by status")
@allure.description("This test ensures that it's possible to get a pet by status.")
@pytest.mark.parametrize(
    "status, expected_names",
    [
        ("available", ["Buddy"]),
        ("pending", ["Whiskers"]),
        ("sold", ["Harvey"]),
        ("in transit", []),
    ],
)
def test_find_pets_by_status(status, expected_names, base_url):
    logger.info(f"Running test: test_find_pets_by_status with status: {status}")
    response = httpx.get(f"{base_url}/pet/findByStatus?status={status}")
    if not expected_names:
        assert (
            response.status_code == 404
        ), f"Unexpected status code: {response.status_code}"
        assert response.json()["detail"] == "Pets not found"
        logger.info(
            f"Test passed: test_find_pets_by_status with status: {status} (empty list)"
        )
    else:
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"
        pets_data = response.json()
        actual_names = [pet["name"] for pet in pets_data]
        assert actual_names == expected_names
        logger.info(f"Test passed: test_find_pets_by_status with status: {status}")


@allure.title("Test for creating a pet")
@allure.description("This test ensures that creating a pet works correctly.")
@pytest.mark.asyncio
async def test_add_pet(base_url):
    logger.info("Running test: test_add_pet")
    new_pet_data = {
        "name": "Max",
        "category": {"id": 3, "name": "Lizards"},
        "status": "available",
    }
    logger.debug(f"Adding new pet: {new_pet_data}")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/pet", json=new_pet_data)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")

        assert (
            response.status_code == 201
        ), f"Unexpected status code: {response.status_code}"

        response_data = response.json()
        assert "id" in response_data, "Response must contain an ID for the new pet"
        assert response_data["name"] == new_pet_data["name"]
        assert response_data["category"]["id"] == new_pet_data["category"]["id"]
        assert response_data["category"]["name"] == new_pet_data["category"]["name"]
        assert response_data["status"] == new_pet_data["status"]
        logger.info(f"Test passed: test_add_pet with new pet ID: {response_data['id']}")


@allure.title("Test for updating data of existing pet")
@allure.description(
    "This test ensures that updating existing pet data works correctly."
)
def test_update_existing_pet(base_url):
    logger.info("Running test: test_update_existing_pet")
    updated_data = {"id": 1, "name": "Buddy Updated", "status": "pending"}
    logger.debug(f"Updating pet: {updated_data}")
    response = httpx.put(f"{base_url}/pet", json=updated_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    updated_pet = response.json()
    assert updated_pet == {
        "id": 1,
        "name": "Buddy Updated",
        "status": "pending",
        "category": {"id": 1, "name": "Dogs"},
    }
    logger.info("Test passed: test_update_existing_pet")


@allure.title("Test for updating data of non-existing pet")
@allure.description(
    "This test ensures that it's not possible to update an non-existing pet data."
)
def test_update_nonexistent_pet(base_url):
    logger.info("Running test: test_update_nonexistent_pet")
    updated_data = {"id": 999, "name": "Ghost Pet", "status": "available"}
    logger.debug(f"Updating pet: {updated_data}")
    response = httpx.put(f"{base_url}/pet", json=updated_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    error_data = response.json()
    assert error_data == {"detail": "Pet not found"}
    logger.info("Test passed: test_update_nonexistent_pet")


@allure.title("Test for updating existing pet with invalid data")
@allure.description(
    "This test ensures that it's not possible to update an existing pet with invalid data format."
)
def test_update_with_invalid_data(base_url):
    logger.info("Running test: test_update_with_invalid_data")
    response = httpx.put(f"{base_url}/pet", content="Not a JSON")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 422
    ), f"Unexpected status code: {response.status_code}"
    logger.info("Test passed: test_update_with_invalid_data")


@allure.title("Test for updating existing pet with form")
@allure.description("This test ensures that update a pet with form works correctly.")
def test_update_pet_with_form_success(base_url):
    logger.info("Running test: test_update_pet_with_form_success")
    pet_id = 1
    form_data = {"name": "Updated Buddy", "status": "updated"}
    logger.debug(f"Updating pet with form data: {form_data}")
    response = httpx.post(f"{base_url}/pet/{pet_id}", data=form_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data["message"] == "Pet updated successfully"
    assert response_data["pet"]["id"] == pet_id
    assert response_data["pet"]["name"] == "Updated Buddy"
    assert response_data["pet"]["status"] == "updated"
    logger.info("Test passed: test_update_pet_with_form_success")


@allure.title("Test for updating non-existing pet with form")
@allure.description(
    "This test ensures that it's not possible to update non-existing pet with form."
)
def test_update_pet_with_form_not_found(base_url):
    logger.info("Running test: test_update_pet_with_form_not_found")
    pet_id = 999
    form_data = {"name": "Ghost Pet", "status": "available"}
    logger.debug(f"Updating pet with form data: {form_data}")
    response = httpx.post(f"{base_url}/pet/{pet_id}", data=form_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["detail"] == "Pet not found"
    logger.info("Test passed: test_update_pet_with_form_not_found")


@allure.title("Test for deleting pet from data")
@allure.description("This test ensures that deleting pet from data works correctly.")
def test_delete_pet_success(base_url):
    logger.info("Running test: test_delete_pet_success")
    pet_id = 1
    response = httpx.delete(f"{base_url}/pet/{pet_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert response_data["message"] == f"Pet with ID {pet_id} has been deleted"

    response = httpx.get(f"{base_url}/pet/{pet_id}")
    logger.debug(f"Response status code after deletion: {response.status_code}")
    logger.debug(f"Response content after deletion: {response.text}")
    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    logger.info("Test passed: test_delete_pet_success")
