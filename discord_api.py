import asyncio
import logging
from typing import List, Optional
from urllib.parse import urljoin
from random import choice

import aiohttp

from user import Friend, MyUser
from utils import load_cache, save_cache

logger = logging.getLogger("rich")


class DiscordAPI:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9153 Chrome/124.0.6367.243 Electron/30.1.0 Safari/537.36",
    ]
    base_headers = {
        "User-Agent": choice(user_agents),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore,
                 token: str, cache_filename: str, date_format: str):
        self.session = session
        self.semaphore = semaphore
        self.token = token
        self.cache_filename = cache_filename
        self.date_format = date_format
        self.headers = self.base_headers | {"Authorization": token}

        self.me: Optional[MyUser] = None

        # Endpoints
        self.relationships_endpoint = "https://discord.com/api/v9/users/@me/relationships"
        self.me_endpoint = "https://discord.com/api/v9/users/@me"

    async def get_relationships(self, cache: bool = True) -> List[Friend]:
        friends = []

        logger.debug("Fetching data from Discord")
        async with self.session.get(self.relationships_endpoint, headers=self.headers) as response:
            response.raise_for_status()
            friends_data = await response.json()

        if cache:
            await save_cache(friends_data, self.cache_filename)

        for friend in friends_data:
            try:
                friends.append(Friend(friend))
            except Exception as e:
                logger.error(f"Failed to parse friend: {friend.username}")
        return friends

    async def delete_user(self, uid: str | int | Friend) -> bool:
        friend: Optional[Friend] = None
        if isinstance(uid, Friend):
            friend = uid
            uid = uid.id

        endpoint = urljoin(self.relationships_endpoint, uid)
        try:
            async with self.semaphore:
                # async with self.session.delete(endpoint, headers=self.headers) as response:
                #     response.raise_for_status()
                #     return response.ok
                if friend is not None:
                    logging.debug(f"{friend.extended_str():<36} [{friend.pretty_since}] Deleted!")
                else:
                    logging.debug(f"User {uid} deleted!")
                await asyncio.sleep(2)
                return True
        except aiohttp.ClientResponseError as e:
            logger.error(f"Failed to delete user {uid}: {e.status} - {e.message}")
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error while trying to delete user {uid}: {e}")
        except Exception as e:
            logger.error(f"Failed to delete user {uid}: {e}")
        return False

    async def get_me(self) -> MyUser:
        if self.me is None:
            try:
                async with self.session.get(self.me_endpoint, headers=self.headers) as response:
                    response.raise_for_status()
                    user_data = await response.json()
                    self.me = MyUser(user_data)
            except aiohttp.ClientResponseError as e:
                logger.error(f"Failed to get user data: {e.status} - {e.message}")
            except aiohttp.ClientConnectionError as e:
                logger.error(f"Connection error while trying to get user data: {e}")
            except Exception as e:
                logger.error(f"Failed to get user data: {e}")
        return self.me

    async def is_valid_token(self) -> bool:
        try:
            if self.me is None:
                await self.get_me()
            return self.me is not None
        except aiohttp.ClientResponseError as e:
            logger.error(f"Failed to validate token: {e.status} - {e.message}")
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error while trying to validate token: {e}")
        except Exception as e:
            logger.error(f"Failed to validate token: {e}")
        return False


if __name__ == "__main__":
    DiscordAPI(55, 5512123, 1231, 123, "123")
