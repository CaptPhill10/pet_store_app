import pytest
import httpx
import logging

logger = logging.getLogger(__name__)


async def add_new_pet(client, base_url):
    """New pet adding"""
    new_pet_data = {
        "name": "Горошек",
        "category": {"id": 4, "name": "Lizards"},
        "status": "available",
    }
    logger.debug(f"Adding new pet with data: {new_pet_data}")
    response = await client.post(f"{base_url}/pet", json=new_pet_data)
    logger.debug(f"Response: {response.status_code}, {response.text}")
    assert response.status_code == 201
    pet_data = response.json()
    logger.info(f"New pet added with ID: {pet_data['id']}")
    return pet_data


async def register_user(client, base_url):
    """New user registration"""
    user_data = {
        "username": "test_user",
        "firstName": "Test",
        "lastName": "User",
        "email": "test_user@example.com",
        "password": "securepassword123",
        "phone": "123456789",
        "userStatus": 1,
    }
    logger.debug(f"Registering new user with data: {user_data}")
    response = await client.post(f"{base_url}/user", json=user_data)
    logger.debug(f"Response: {response.status_code}, {response.text}")
    assert response.status_code == 201
    assert response.json()["username"] == "test_user"
    logger.info("New user registered successfully")
    return user_data


async def login_user(client, base_url, user_data):
    """User login."""
    login_params = {"username": user_data["username"], "password": user_data["password"]}
    logger.debug(f"Logging in user with params: {login_params}")
    response = await client.get(f"{base_url}/user/login", params=login_params)
    logger.debug(f"Response: {response.status_code}, {response.text}")
    assert response.json()["message"] == "Login successful"
    assert response.json()["username"] == user_data["username"]
    logger.info("User logged in successfully")


async def create_order(client, base_url, pet_id):
    """Create an order for a pet"""
    order_data = {
        "petId": pet_id,
        "quantity": 1,
        "shipDate": "2025-01-01T10:00:00.000Z",
        "status": "placed",
        "complete": False,
    }
    logger.debug(f"Creating order with data: {order_data}")
    response = await client.post(f"{base_url}/store/order", json=order_data)
    logger.debug(f"Response: {response.status_code}, {response.text}")
    assert response.status_code == 201
    logger.info("Order created successfully")
    return response.json()


async def update_pet_status(client, base_url, pet_data, new_status):
    """Pet status update"""
    pet_data["status"] = new_status
    logger.debug(f"Updating pet status to '{new_status}': {pet_data}")
    response = await client.put(f"{base_url}/pet", json=pet_data)
    logger.debug(f"Response: {response.status_code}, {response.text}")
    assert response.status_code == 200
    assert response.json()["status"] == new_status
    logger.info(f"Pet status updated to '{new_status}'")


@pytest.mark.asyncio
async def test_pet_order_workflow(base_url):
    """E2E test for full order of the pet with status changes"""
    logger.info("Running test: test_pet_order_workflow")

    async with httpx.AsyncClient() as client:
        # Add pet
        pet_data = await add_new_pet(client, base_url)
        pet_id = pet_data["id"]

        # User registration and login
        user_data = await register_user(client, base_url)
        await login_user(client, base_url, user_data)

        # Order create
        await create_order(client, base_url, pet_id)

        # Pet statuses update
        await update_pet_status(client, base_url, pet_data, "pending")
        await update_pet_status(client, base_url, pet_data, "in delivery")
        await update_pet_status(client, base_url, pet_data, "sold")
