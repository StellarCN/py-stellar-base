import json

__all__ = ["Response"]


class Response:
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.

    :param status_code: response status code
    :param text: response content
    :param headers: response headers
    :param url: request url
    """

    def __init__(self, status_code: int, text: str, headers: dict, url: str) -> None:
        self.status_code: int = status_code
        self.text: str = text
        self.headers: dict = headers
        self.url: str = url

    def json(self) -> dict:
        """convert the content to dict

        :return: the content from server
        """
        return json.loads(self.text)

    def __hash__(self):
        return hash(
            (self.status_code, self.text, tuple(self.headers.items()), self.url)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.status_code == other.status_code
            and self.text == other.text
            and self.headers == other.headers
            and self.url == other.url
        )

    def __repr__(self):
        return (
            f"<Response [status_code={self.status_code}, "
            f"text={self.text}, "
            f"headers={self.headers}, "
            f"url={self.url}]>"
        )
