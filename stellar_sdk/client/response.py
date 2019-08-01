import json


class Response:
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.

    """

    def __init__(self, status_code: int, text: str, headers: dict, url: str) -> None:
        self.status_code = status_code
        self.text = text
        self.headers = headers
        self.url = url

    def json(self) -> dict:
        return json.loads(self.text)

    def __eq__(self, other: 'Response'):
        return self.status_code == other.status_code and self.text == other.text

    def __str__(self):
        return '<Response [%s]>' % self.status_code
