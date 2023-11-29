from .handler import Lookup, Response, ResponseDict
import time
import json
import os


class Cache:
    """
    Represents a cache for storing and retrieving responses based on lookup queries.

    Parameters:
    - dir_path (str): The directory path for storing cache files. Default is the current directory.
    - timeout (int): The timeout duration for considering cache entries stale, in seconds. Default is one week (604800 seconds).

    Attributes:
    - __dir_path (str): The directory path for storing cache files.
    - __timeout (int): The timeout duration for considering cache entries stale, in seconds.
    - __last_checked (str | None): The path of the last checked cache file or None if not checked.
    - __responses (dict[Lookup, list[Response]]): A dictionary to store responses based on lookup queries.

    Methods:
    - is_stale(lookup: Lookup) -> bool: Checks if the cache entry for a given lookup is stale.
    - get_last_checked() -> str | None: Returns the path of the last checked cache file.
    - erase_last_checked() -> None: Deletes the last checked cache file.
    - feed(lookup: Lookup, response: Response) -> None: Adds a response to the cache for a given lookup.
    - commit() -> None: Commits the cached responses to files.
    - fetch(cache_path: str) -> list[ResponseDict]: Reads and returns responses from a cache file.
    """

    def __init__(self, dir_path: str = ".", timeout: int = 604800) -> None:
        self.__dir_path = f"{dir_path}/cache"
        self.__timeout = timeout
        self.__last_checked: str | None = None
        self.__responses: dict[Lookup, list[Response]] = {}

    def is_stale(self, lookup: Lookup) -> bool:
        """
        Checks if the cache entry for a given lookup is stale.

        Parameters:
        - lookup (Lookup): The lookup object for which to check the cache.

        Returns:
        - bool: True if the cache entry is stale, False otherwise.
        """

        cache_dir = f"{self.__dir_path}/{lookup.query}"

        if os.path.exists(cache_dir) and os.listdir(cache_dir):
            cache_file = os.listdir(cache_dir)[0]
            self.__last_checked = f"{cache_dir}/{cache_file}"

            timestamp_str, extension = cache_file.split("_")
            count_str = extension.split(".")[0]

            cached_timestamp = int(timestamp_str)
            cached_count = int(count_str)

            required_count = int(lookup.count - 0.05 * lookup.count)

            if cached_timestamp < int(time.time() - self.__timeout):
                return True
            else:
                return required_count > cached_count

        return True

    def get_last_checked(self) -> str | None:
        """
        Returns the path of the last checked cache file.

        Returns:
        - str | None: The path of the last checked cache file or None if not checked.
        """

        return self.__last_checked

    def erase_last_checked(self) -> None:
        """
        Deletes the last checked cache file.
        """

        if self.__last_checked is not None and os.path.exists(self.__last_checked):
            cache_dir = os.path.dirname(self.__last_checked)
            for cache_file in os.listdir(cache_dir):
                os.remove(f"{cache_dir}/{cache_file}")

    def feed(self, lookup: Lookup, response: Response) -> None:
        """
        Adds a response to the cache for a given lookup.

        Parameters:
        - lookup (Lookup): The lookup object for which to add the response.
        - response (Response): The response to be added to the cache.
        """

        if lookup in self.__responses:
            self.__responses[lookup].append(response)
        else:
            self.__responses[lookup] = [response]

    def commit(self) -> None:
        """
        Commits the cached responses to files.
        """

        for lookup in self.__responses:
            data = [response.to_dict() for response in self.__responses[lookup]]

            cache_dir = f"{self.__dir_path}/{lookup.query}"
            os.makedirs(cache_dir, exist_ok=True)

            cache_path = f"{cache_dir}/{int(time.time())}_{len(data)}.json"
            with open(cache_path, "w") as fw:
                json.dump(data, fw)

        self.__responses = {}

    def fetch(self, cache_path: str) -> list[ResponseDict]:
        """
        Reads and returns responses from a cache file.

        Parameters:
        - cache_path (str): The path to the cache file.

        Returns:
        - list[ResponseDict]: The list of responses read from the cache file.
        """

        with open(cache_path, "r") as fr:
            return json.load(fr)
