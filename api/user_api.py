from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from data.user_data import users as init_users
from util.logging_config import logger

router = APIRouter()


# User data model
class User(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: int = 0  # 0 - active user, 1 - inactive user


class NewUser(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str


# User storage structure
class UserStore:
    def __init__(self, init_users):
        self.users = init_users

    def add_user(self, user: NewUser):
        logger.info("Adding new user", user=user.model_dump())
        new_id = max([u["id"] for u in self.users]) + 1 if self.users else 1
        user_data = user.model_dump()
        user_data["id"] = new_id
        self.users.append(user_data)
        logger.info("Added new user with ID", user_id=new_id)
        return user_data

    def get_user_by_username(self, username: str):
        logger.info("Searching for user", username=username)
        user = next((u for u in self.users if u["username"] == username), None)
        if not user:
            logger.warning("User not found", username=username)
        return user

    def update_user(self, username: str, user: User):
        logger.info("Updating user", username=username, user=user.model_dump())
        existing_user = self.get_user_by_username(username)
        if not existing_user:
            logger.error("User not found", username=username)
            raise HTTPException(status_code=404, detail="User not found")
        existing_user.update(user.model_dump())
        logger.info("User updated successfully", username=username)
        return existing_user

    def delete_user(self, username: str):
        logger.info("Deleting user", username=username)
        existing_user = self.get_user_by_username(username)
        if not existing_user:
            logger.error("User not found", username=username)
            raise HTTPException(status_code=404, detail="User not found")
        self.users = [u for u in self.users if u["username"] != username]
        logger.info("User deleted successfully", username=username)
        return {"message": f"User with username {username} has been deleted"}

    def login_user(self, username: str, password: str):
        logger.info("Logging in user", username=username)
        user = self.get_user_by_username(username)
        if not user:
            logger.error("User not found", username=username)
            raise HTTPException(status_code=404, detail="User not found")
        if user["password"] != password:
            logger.error("Invalid username or password", username=username)
            raise HTTPException(status_code=401, detail="Invalid username or password")
        logger.info("User logged in successfully", username=username)
        return {"message": "Login successful", "username": username}

    def logout_user(self):
        logger.info("User logged out successfully")
        return {"message": "Logout successful"}

    def create_users(self, users: List[NewUser]):
        logger.info("Creating multiple users", count=len(users))
        new_users = []
        for user in users:
            new_users.append(self.add_user(user))
        logger.info("Users created successfully", count=len(new_users))
        return {
            "message": f"{len(new_users)} users created successfully",
            "users": new_users,
        }


user_store = UserStore(init_users)


@router.post("/user", response_model=Dict, status_code=201)
def add_user(user: NewUser):
    logger.info("Received request to add new user", user=user.model_dump())
    return user_store.add_user(user)


@router.get("/user/login", response_model=Dict)
def login_user(username: str, password: str):
    logger.info("Received request to login user", username=username)
    return user_store.login_user(username, password)


@router.get("/user/logout", response_model=Dict)
def logout_user():
    logger.info("Received request to logout user")
    return user_store.logout_user()


@router.get("/user/{username}", response_model=Dict)
def get_user(username: str):
    logger.info("Received request to get user by username", username=username)
    user = user_store.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/{username}", response_model=Dict)
async def update_user(username: str, user: User):
    logger.info(
        "Received request to update user", username=username, user=user.model_dump()
    )
    return user_store.update_user(username, user)


@router.delete("/user/{username}")
def delete_user(username: str):
    logger.info("Received request to delete user", username=username)
    return user_store.delete_user(username)


@router.post("/user/createWithList", response_model=Dict)
async def create_users_with_list(users: List[NewUser]):
    logger.info("Received request to create users with list", count=len(users))
    return user_store.create_users(users)


@router.post("/user/createWithArray", response_model=Dict)
async def create_users_with_array(users: List[NewUser]):
    logger.info("Received request to create users with array", count=len(users))
    return user_store.create_users(users)


# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Dict, List
# from data.user_data import users as init_users
# import logging
#
# logger = logging.getLogger(__name__)
#
# router = APIRouter()
#
#
# # User data model
# class User(BaseModel):
#     id: int
#     username: str
#     firstName: str
#     lastName: str
#     email: str
#     password: str
#     phone: str
#     userStatus: int = 0  # 0 - active user, 1 - inactive user
#
#
# class NewUser(BaseModel):
#     username: str
#     firstName: str
#     lastName: str
#     email: str
#     password: str
#     phone: str
#
#
# # User storage structure
# class UserStore:
#     def __init__(self, init_users):
#         self.users = init_users
#
#     def add_user(self, user: NewUser):
#         logger.info(f"Adding new user: {user.dict()}")
#         new_id = max([u["id"] for u in self.users]) + 1 if self.users else 1
#         user_data = user.dict()
#         user_data["id"] = new_id
#         self.users.append(user_data)
#         logger.info(f"Added new user with ID: {new_id}")
#         return user_data
#
#     def get_user_by_username(self, username: str):
#         logger.info(f"Searching for user: {username}")
#         user = next((u for u in self.users if u["username"] == username), None)
#         if not user:
#             logger.warning(f"User with username {username} not found")
#         return user
#
#     def update_user(self, username: str, user: User):
#         logger.info(f"Updating user with username: {username}")
#         existing_user = self.get_user_by_username(username)
#         if not existing_user:
#             logger.error(f"User with username {username} not found")
#             raise HTTPException(status_code=404, detail="User not found")
#         existing_user.update(user.dict())
#         logger.info(f"User with username {username} updated successfully")
#         return existing_user
#
#     def delete_user(self, username: str):
#         logger.info(f"Deleting user with username: {username}")
#         existing_user = self.get_user_by_username(username)
#         if not existing_user:
#             logger.error(f"User with username {username} not found")
#             raise HTTPException(status_code=404, detail="User not found")
#         self.users = [u for u in self.users if u["username"] != username]
#         logger.info(f"User with username {username} deleted successfully")
#         return {"message": f"User with username {username} has been deleted"}
#
#     def login_user(self, username: str, password: str):
#         logger.info(f"Logging in user: {username}")
#         user = self.get_user_by_username(username)
#         if not user:
#             logger.error(f"User with username {username} not found")
#             raise HTTPException(status_code=404, detail="User not found")
#         if user["password"] != password:
#             logger.error(f"Invalid username or password for user: {username}")
#             raise HTTPException(status_code=401, detail="Invalid username or password")
#         logger.info(f"User {username} logged in successfully")
#         return {"message": "Login successful", "username": username}
#
#     def logout_user(self):
#         logger.info("User logged out successfully")
#         return {"message": "Logout successful"}
#
#     def create_users(self, users: List[NewUser]):
#         logger.info(f"Creating multiple users: {[user.dict() for user in users]}")
#         new_users = []
#         for user in users:
#             new_users.append(self.add_user(user))
#         logger.info(f"{len(new_users)} users created successfully")
#         return {"message": f"{len(new_users)} users created successfully", "users": new_users}
#
#
# user_store = UserStore(init_users)
#
#
# @router.post("/user", response_model=Dict, status_code=201)
# def add_user(user: NewUser):
#     logger.info(f"Received request to add new user: {user.dict()}")
#     return user_store.add_user(user)
#
#
# @router.get("/user/login", response_model=Dict)
# def login_user(username: str, password: str):
#     logger.info(f"Received request to login user: {username}")
#     return user_store.login_user(username, password)
#
#
# @router.get("/user/logout", response_model=Dict)
# def logout_user():
#     logger.info("Received request to logout user")
#     return user_store.logout_user()
#
#
# @router.get("/user/{username}", response_model=Dict)
# def get_user(username: str):
#     logger.info(f"Received request to get user by username: {username}")
#     user = user_store.get_user_by_username(username)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# @router.put("/user/{username}", response_model=Dict)
# async def update_user(username: str, user: User):
#     logger.info(f"Received request to update user: {username}")
#     return user_store.update_user(username, user)
#
#
# @router.delete("/user/{username}")
# def delete_user(username: str):
#     logger.info(f"Received request to delete user: {username}")
#     return user_store.delete_user(username)
#
#
# @router.post("/user/createWithList", response_model=Dict)
# async def create_users_with_list(users: List[NewUser]):
#     logger.info(f"Received request to create users with list: {[user.dict() for user in users]}")
#     return user_store.create_users(users)
#
#
# @router.post("/user/createWithArray", response_model=Dict)
# async def create_users_with_array(users: List[NewUser]):
#     logger.info(f"Received request to create users with array: {[user.dict() for user in users]}")
#     return user_store.create_users(users)
