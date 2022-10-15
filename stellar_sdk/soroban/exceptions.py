from typing import Optional

from ..exceptions import SdkError


# TODO: define more specific exceptions
class RequestException(SdkError):
    def __init__(self, code: int, message: Optional[str]):
        self.code = code
        self.message = message
        super().__init__(
            f"<RequestException [code={self.code}, message={self.message}]>"
        )
        # data: Optional[E]
