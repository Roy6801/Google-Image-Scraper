from typing import Literal, Union, Generator, Any
from .util import query_cleaner
from queue import Queue
import time

ResponseDict = dict[
    Literal[
        "query", "name", "src_name", "src_page", "thumbnail", "image", "width", "height"
    ],
    Union[str, int, None],
]


class Lookup:
    """
    Represents a lookup request with a query and count.

    Parameters:
    - query (str): The query string to be looked up.
    - count (int): The count of results to retrieve.

    Attributes:
    - query (str): The cleaned query string.
    - count (int): The count of results to retrieve.
    """

    def __init__(self, query: str, count: int) -> None:
        self.query = query_cleaner(query)
        self.count = count


class Response:
    """
    Represents a response with various attributes.

    Parameters:
    - query (str): The query associated with the response.
    - name (str): The name attribute of the response.
    - src_name (str): The source name attribute of the response.
    - src_page (str): The source page attribute of the response.
    - thumbnail (str): The thumbnail attribute of the response.
    - image (str): The image attribute of the response.
    - width (int): The width attribute of the response.
    - height (int): The height attribute of the response.

    Attributes:
    - query (str): The query associated with the response.
    - name (str): The name attribute of the response.
    - src_name (str): The source name attribute of the response.
    - src_page (str): The source page attribute of the response.
    - thumbnail (str): The thumbnail attribute of the response.
    - image (str): The image attribute of the response.
    - width (int): The width attribute of the response.
    - height (int): The height attribute of the response.

    Methods:
    - to_dict(): Converts the response attributes to a dictionary.

    Returns:
    - Response: An instance of the Response class.
    """

    def __init__(
        self,
        query=None,
        name=None,
        src_name=None,
        src_page=None,
        thumbnail=None,
        image=None,
        width=None,
        height=None,
    ) -> None:
        self.query = query
        self.name = name
        self.src_name = src_name
        self.src_page = src_page
        self.thumbnail = thumbnail
        self.image = image
        self.width = width
        self.height = height

    def to_dict(self) -> ResponseDict:
        """
        Converts the response attributes to a dictionary.

        Returns:
        - ResponseDict: A dictionary containing the response attributes.
        """

        return {
            "query": self.query,
            "name": self.name,
            "src_name": self.src_name,
            "src_page": self.src_page,
            "thumbnail": self.thumbnail,
            "image": self.image,
            "width": self.width,
            "height": self.height,
        }


class QueueStream:
    """
    Represents a stream for processing items from a queue.

    Parameters:
    - queue (Queue): The queue to process items from.
    - timeout (int): The timeout for waiting for items in the queue.
    - initial_timeout (int): The initial timeout for waiting for items in the queue.

    Attributes:
    - __queue (Queue): The queue to process items from.
    - __timeout (int): The timeout for waiting for items in the queue.
    - __initial_timeout (int): The initial timeout for waiting for items in the queue.

    Methods:
    - get(): Generator method for retrieving items from the queue as Response objects.

    Yields:
    - Response: An instance of the Response class.
    """

    def __init__(
        self, queue: Queue, timeout: int = 10, initial_timeout: int = 30
    ) -> None:
        self.__queue = queue
        self.__timeout = timeout
        self.__initial_timeout = initial_timeout

    def get(self) -> Generator[Response, Any, None]:
        """
        Generator method for retrieving items from the queue as Response objects.

        Yields:
        - Response: An instance of the Response class.
        """

        last_fetch = time.time()
        wait_time = 0

        timeout = self.__initial_timeout

        while wait_time < timeout:
            if not self.__queue.empty():
                timeout = self.__timeout
                item = self.__queue.get()
                if isinstance(item, Response):
                    yield item
                last_fetch = time.time()
                wait_time = 0
            else:
                wait_time = time.time() - last_fetch


class CacheStream:
    """
    Represents a stream for processing items from a cached list of responses.

    Parameters:
    - responses (list[ResponseDict]): The list of cached responses.

    Attributes:
    - __responses (list[ResponseDict]): The list of cached responses.

    Methods:
    - get(): Generator method for retrieving items from the cached responses as Response objects.

    Yields:
    - Response: An instance of the Response class.
    """

    def __init__(self, responses: list[ResponseDict]) -> None:
        self.__responses = responses

    def get(self) -> Generator[Response, Any, None]:
        """
        Generator method for retrieving items from the cached responses as Response objects.

        Yields:
        - Response: An instance of the Response class.
        """

        for item in self.__responses:
            yield Response(**item)
