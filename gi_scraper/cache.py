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
            timestamp_dirs = os.listdir(cache_dir)
            max_timestamp = max(map(int, timestamp_dirs))
            timestamp_dir = os.path.join(cache_dir, str(max_timestamp))
            counts = os.listdir(timestamp_dir)
            max_count = max(map(lambda x: int(x.split(".")[0]), counts))
            cache_file = os.path.join(timestamp_dir, f"{max_count}.json")
            self.__last_checked = cache_file

            if max_timestamp < int(time.time() - self.__timeout):
                return True
            else:
                if counts:
                    required_count = int(lookup.count - 0.05 * lookup.count)
                    return required_count > max_count
                else:
                    return True
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
            timestamp_dir = os.path.dirname(self.__last_checked)
            cache_dir = os.path.dirname(timestamp_dir)
            for timestamp_dir_name in os.listdir(cache_dir):
                timestamp_dir = os.path.join(cache_dir, timestamp_dir_name)
                for cache_name in os.listdir(timestamp_dir):
                    cache_file = os.path.join(timestamp_dir, cache_name)
                    os.remove(cache_file)
                os.rmdir(timestamp_dir)

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

            cache_dir = os.path.join(
                self.__dir_path, lookup.query, str(int(time.time()))
            )
            os.makedirs(cache_dir, exist_ok=True)

            cache_path = os.path.join(cache_dir, f"{len(data)}.json")
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
