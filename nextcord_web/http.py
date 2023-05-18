from __future__ import annotations

from typing import ClassVar, Optional, Any, TYPE_CHECKING, Type

from urllib.parse import quote
from aiohttp import ClientSession

from .enums import Discord
from .errors import UnsupportedApiVersion
from .types import API_VERSION, Client

if TYPE_CHECKING:
    from . import Snowflake, API_VERSION


class Route:
    BASE: ClassVar[str] = "https://discord.com/api/v{}"

    def __init__(self, method: str, path: str, api_version: API_VERSION, **parameters: Any) -> None:
        BASE: str = self.BASE.format(api_version)

        self.path: str = path
        self.method: str = method
        url = BASE + self.path
        if parameters:
            url = url.format_map(
                {k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()}
            )
        self.url: str = url

        # major parameters:
        self.channel_id: Optional[Snowflake] = parameters.get("channel_id")
        self.guild_id: Optional[Snowflake] = parameters.get("guild_id")
        self.webhook_id: Optional[Snowflake] = parameters.get("webhook_id")
        self.webhook_token: Optional[str] = parameters.get("webhook_token")

    @property
    def bucket(self) -> str:
        # the bucket is just method + path w/ major parameters
        return f"{self.channel_id}:{self.guild_id}:{self.path}"


class HTTPClient:
    __version__: str = "1.0a1"

    def __init__(
            self,
            bot: Client,
            secret_key: str,
            api_version: API_VERSION = 10,
            host: str = "localhost",
            port: int = 9000) -> None:

        if api_version not in (9, 10):
            raise UnsupportedApiVersion

        self._secret_key: str = secret_key
        self._HTTPClient = ClientSession()
        self._base_url: str = Discord.BASE_URL.value.format(api_version)
        self._bot: Client = bot
        self._api_version: API_VERSION = api_version
        self.Route: Type[Route] = Route

        self.host: str = host
        self.port: int = port




