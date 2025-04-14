import allure
import httpx
import pytest

from util.logging_config import logger


@allure.title("Test for creating a new user")
@allure.description(
    "This test ensures that a user is created successfully with valid input data."
)
def test_create_user(base_url):
    logger.info("Running test: test_create_user")
    user_data = {
        "username": "casper_schmeihel",
        "firstName": "Casper",
        "lastName": "Schmeihel",
        "email": "casper_schmeihel@example.com",
        "password": "securepassword",
        "phone": "123-456-7890",
    }
    logger.debug(f"Creating user with data: {user_data}")
    response = httpx.post(f"{base_url}/user", json=user_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["username"] == "casper_schmeihel"
    logger.info("Test passed: test_create_user")


@allure.title("Test for retrieving user information")
@allure.description(
    "This test checks that user information is retrieved successfully by username."
)
def test_get_user_info(base_url):
    logger.info("Running test: test_get_user_info")
    username = "percival_de_rolo"
    logger.debug(f"Getting user by username: {username}")
    response = httpx.get(f"{base_url}/user/{username}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["username"] == username
    logger.info("Test passed: test_get_user_info")


@allure.title("Test for updating existing user")
@allure.description(
    "This test verifies that an existing user's data can be updated correctly."
)
def test_available_user_update(base_url):
    logger.info("Running test: test_available_user_update")
    username = "percival_de_rolo"
    updated_data = {
        "id": 1,
        "username": "percival_de_rolo",
        "firstName": "Percival",
        "lastName": "de Rolo",
        "email": "percival_de_rolo_updated@example.com",
        "password": "newpassword",
        "phone": "123-456-7890",
        "userStatus": 0,
    }
    logger.debug(f"Updating user with data: {updated_data}")
    response = httpx.put(f"{base_url}/user/{username}", json=updated_data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["email"] == "percival_de_rolo_updated@example.com"
    logger.info("Test passed: test_available_user_update")


@allure.title("Test for deleting a user")
@allure.description(
    "This test ensures that a user is successfully deleted and returns the expected message."
)
def test_delete_user(base_url):
    logger.info("Running test: test_delete_user")
    username = "percival_de_rolo"
    logger.debug(f"Deleting user with username: {username}")
    response = httpx.delete(f"{base_url}/user/{username}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json() == {
        "message": f"User with username {username} has been deleted"
    }
    logger.info("Test passed: test_delete_user")


@allure.title("Test for successful user login")
@allure.description("This test checks that a user can log in with correct credentials.")
def test_login_user_success(base_url):
    logger.info("Running test: test_login_user_success")

    username = "keyleth_ashari"
    password = "securepass"
    logger.debug(f"Logging in user: {username} with password: {password}")
    response = httpx.get(
        f"{base_url}/user/login", params={"username": username, "password": password}
    )
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["message"] == "Login successful"
    assert response.json()["username"] == username
    logger.info("Test passed: test_login_user_success")


@allure.title("Test for failed user login")
@allure.description(
    "This test verifies that login fails when incorrect credentials are provided."
)
def test_login_user_failure(base_url):
    logger.info("Running test: test_login_user_failure")
    username = "keyleth_ashari"
    password = "wrongpassword"
    logger.debug(f"Logging in user: {username} with password: {password}")
    response = httpx.get(
        f"{base_url}/user/login", params={"username": username, "password": password}
    )
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 401
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["detail"] == "Invalid username or password"
    logger.info("Test passed: test_login_user_failure")


@allure.title("Test for logging out a user")
@allure.description("This test ensures that a user is logged out successfully.")
def test_logout_user(base_url):
    logger.info("Running test: test_logout_user")
    response = httpx.get(f"{base_url}/user/logout")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["message"] == "Logout successful"
    logger.info("Test passed: test_logout_user")


@allure.title("Test for creating users with a list")
@allure.description(
    "This test checks that multiple users can be created from a list payload."
)
@pytest.mark.asyncio
async def test_create_users_with_list(base_url):
    logger.info("Running test: test_create_users_with_list")
    users_data = [
        {
            "username": "alice",
            "firstName": "Alice",
            "lastName": "Wonder",
            "email": "alice@example.com",
            "password": "alicepassword",
            "phone": "111-111-1111",
        },
        {
            "username": "bob",
            "firstName": "Bob",
            "lastName": "Builder",
            "email": "bob@example.com",
            "password": "bobpassword",
            "phone": "222-222-2222",
        },
    ]
    logger.debug(f"Creating users with list: {users_data}")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/user/createWithList", json=users_data)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"
        assert response.json()["message"] == "2 users created successfully"
        assert len(response.json()["users"]) == 2
    logger.info("Test passed: test_create_users_with_list")


@allure.title("Test for creating users with an array")
@allure.description("This test verifies user creation using an array of user data.")
@pytest.mark.asyncio
async def test_create_users_with_array(base_url):
    logger.info("Running test: test_create_users_with_array")
    users_data = [
        {
            "username": "charlie",
            "firstName": "Charlie",
            "lastName": "Brown",
            "email": "charlie@example.com",
            "password": "charliepassword",
            "phone": "333-333-3333",
        }
    ]
    logger.debug(f"Creating users with array: {users_data}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/user/createWithArray", json=users_data
        )
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        assert (
            response.status_code == 200
        ), f"Unexpected status code: {response.status_code}"
        assert response.json()["message"] == "1 users created successfully"
        assert len(response.json()["users"]) == 1
    logger.info("Test passed: test_create_users_with_array")
