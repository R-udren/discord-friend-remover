import json
import logging
import os
import time
from contextlib import contextmanager
from datetime import datetime
from typing import List

from rich.logging import RichHandler

logger = logging.getLogger("rich")


def setup_logging():
    logging.basicConfig(
        level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(show_path=False)]
    )
    global logger
    logger = logging.getLogger("rich")
    return logger


@contextmanager
def measure_execution_time():
    start_time = time.time()
    yield
    end_time = time.time()
    logger.info(f"Время выполнения: {end_time - start_time:.2f} секунд")


def load_cache(cache_filename: str) -> dict:
    if not os.path.exists(cache_filename):
        return {}
    with open(cache_filename, "r") as file:
        return json.load(file)


async def save_cache(friends: List[dict], cache_filename: str):
    total_friends = len(friends)
    data = {
        "date": datetime.now().isoformat(),
        "friends": friends,
        "total_friends": total_friends,
    }
    with open(cache_filename, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logger.debug(f"Cached data successfully! 📦 ({total_friends} friends)")
