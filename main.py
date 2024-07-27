import asyncio
import logging
import os

import aiohttp
from dotenv import load_dotenv

from discord_api import DiscordAPI
from utils import measure_execution_time, setup_logging

load_dotenv()

# Global constants
CACHE_FILENAME = "friends_cache.json"
DATE_FORMAT = "%H:%M %d.%m.%Y"
TOKEN = os.getenv("DISCORD_TOKEN")
WHITE_LIST = [username.strip() for username in os.getenv("WHITE_LIST", "").split(",")]
RATE_LIMIT = 100

# Configure logging
setup_logging()
logger = logging.getLogger("rich")


async def main():
    semaphore = asyncio.Semaphore(RATE_LIMIT)
    logger.debug(f"Токен: {TOKEN[:5]}...")
    logger.info(f"Белый список: {', '.join(WHITE_LIST)}")

    async with aiohttp.ClientSession() as session:
        api = DiscordAPI(session, semaphore, TOKEN, CACHE_FILENAME, DATE_FORMAT)

        # Check if token is valid and get user info
        if not await api.is_valid_token():
            logger.error("Invalid token! Please check your discord token.")
            return
        else:
            logger.info(f"Твой пользователь: {api.me}")

        friends = await api.get_relationships(cache=True)

        friends_to_delete = [
            friend for friend in friends
            if friend.is_friend and friend.username not in WHITE_LIST and friend.global_name not in WHITE_LIST
        ]

        logger.info(f"У тебя всего {len(friends)} друзей! Друзей к удалению: {len(friends_to_delete)}")

        delete_tasks = [api.delete_user(friend) for friend in friends_to_delete]
        results = await asyncio.gather(*delete_tasks)

    logger.info(f"Удалено {len([res for res in results if res])} друзей из {len(friends)}.")
    logger.info(f"Осталось {len(friends) - len([res for res in results if res])} друзей.")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with measure_execution_time():
        asyncio.run(main())
