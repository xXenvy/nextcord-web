from .http import HTTPClient

from .types import Client, API_VERSION, Guild
from typing import List


class WebClient(HTTPClient):

    def __init__(self, bot: Client, secret_key: str, api_version: API_VERSION = 10) -> None:
        super().__init__(bot=bot, secret_key=secret_key, api_version=api_version)

    @property
    def guilds(self) -> List[Guild]:
        return self._bot.guilds