import logging
from gnl_api_framework.services.base_service import BaseGNLBackendService
from gnl_api_framework.model.user import User

logger = logging.getLogger(__name__)

class UserService(BaseGNLBackendService):
    def getUserByDiscord(self, discord_name):
        if not discord_name:
            logger.error(f"Discord name not defined: {discord_name}")
            raise Exception(f"Discord name not defined: {discord_name}")
        logger.debug(f"Searching for user by Discord name: {discord_name}")
        users = self.search_users(f"discordTag=={discord_name}")
        if not users or len(users) == 0:
            logger.debug(f"No user found with Discord name: {discord_name}")
            return None
        if len(users) > 1:
            logger.error(f"More than one user found with Discord name: {discord_name}")
            raise Exception(f"More than one user found by Discord name: {discord_name}")
        user = users[0]
        logger.debug(f"Found user: {user}")
        return user

    def search_users(self, search_string, limit: int = None, offset: int = None):
        if not search_string:
            logger.error(f"Search String not defined: {search_string}")
            raise Exception(f"Search String not defined: {search_string}")
        logger.debug(f"Searching users with query: {search_string}")
        users = self.search("users/search", search_string, limit=limit, offset=offset)
        logger.debug(f"Received response: {users}")
        l = [User(user) for user in users]
        return l

    def get_user(self, user_id: int):
        logger.debug(f"Fetching user with ID: {user_id}")
        result = self.get(f"users/{user_id}")
        logger.debug(f"Received response: {result}")
        return User(result)

    def update_user(self, user_id, user: User):
        if not user or not user_id:
            logger.error(f"User or user ID not defined: {user}")
            raise Exception(f"User or user id not defined: {user}")
        logger.debug(f"Updating user with ID: {user_id}, data: {user.to_dict()}")
        result = self.put(f"users/{user_id}", user.to_dict())
        logger.debug(f"Received response: {result}")
        return User(result)

    def create_user(self, user: User):
        if not user:
            logger.error(f"User not defined: {user}")
            raise Exception(f"User not defined: {user}")
        logger.debug(f"Creating new user with data: {user.to_dict()}")
        result = self.post("users", user.to_dict())
        logger.debug(f"Received response: {result}")
        return User(result)

    def delete_user(self, user_id):
        if not user_id:
            logger.error(f"User ID not defined: {user_id}")
            raise Exception(f"User id not defined: {user_id}")
        logger.debug(f"Deleting user with ID: {user_id}")
        self.delete(f"users/{user_id}")
        logger.debug(f"User with ID {user_id} deleted successfully")
        return True

    def get_all_users(self, limit: int = None, offset: int = None):
        logger.debug("Fetching all users")
        users = self.get("users", limit=limit, offset=offset)
        logger.debug(f"Received response: {users}")
        l = [User(user) for user in users]
        return l
