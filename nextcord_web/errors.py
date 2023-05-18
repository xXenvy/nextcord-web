

__all__: tuple[str, ...] = (
    "UnsupportedApiVersion",
    "NextcordWebException"
)


class NextcordWebException(Exception):
    pass


class UnsupportedApiVersion(NextcordWebException):

    def __init__(self) -> None:
        super().__init__(
            "Invalid Api Version. Currently supported versions: 10, 9"
        )