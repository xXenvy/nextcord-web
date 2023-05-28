from .http import HTTPClient

from .types import Client, API_VERSION, Guild
from typing import List
import aiohttp.web
from asyncio import get_event_loop


class IpcServerResponse:
    def __init__(self, data):
        self._json = data
        self.length = len(data)

        self.endpoint = data["endpoint"]

        for key, value in data["data"].items():
            setattr(self, key, value)

    def to_json(self):
        return self._json

    def __repr__(self):
        return "<IpcServerResponse length={0.length}>".format(self)

    def __str__(self):
        return self.__repr__()


class WebServer(HTTPClient):

    def __init__(self, bot: Client, secret_key: str, api_version: API_VERSION = 10, host: str = "127.0.0.1", port: int = 9000) -> None:
        super().__init__(bot=bot, secret_key=secret_key, api_version=api_version, host=host, port=port)

        self.loop = bot.loop
        self.endpoints: dict = {"/get_bot": self._get_bot}

    async def __start(self, application, port):
        runner = aiohttp.web.AppRunner(application)
        await runner.setup()

        site = aiohttp.web.TCPSite(runner, self.host, port)
        await site.start()

    def convert(self, data: dict) -> dict:
        _result: dict = {}

        for key, value in data.items():
            if type(value) in (str, int, bool):
                _result[key] = value

        return _result

    async def _get_bot(self):
        data = self.convert(self._bot.__dict__)
        __guilds: dict = {}

        for guild in self._bot.guilds:

            __guilds[guild.id] = {"guild_name": guild.name,
                              "guild_members": guild.member_count,
                              "guild_owner": guild.owner.id}
        data["guilds"] = __guilds

        return data

    async def handle(self, request):
        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(request)

        async for message in websocket:
            request = message.json()
            headers = request.get("headers")
            endpoint = request.get("endpoint")
            print(endpoint)

            if not headers or headers.get("Authorization") != self._secret_key:
                response = {"error": "Invalid or no token provided.", "code": 403}
            else:
                server_response = IpcServerResponse(request)

                try:
                    ret = self.endpoints.get(endpoint)
                    response = await ret()
                except Exception as error:
                    print(error)

                    response = {
                        "error": "IPC route raised error of type {}".format(
                            type(error).__name__
                        ),
                        "code": 500,
                    }
            print(response)
            await websocket.send_json(response)

    async def run(self):
        self._server = aiohttp.web.Application()
        self._server.router.add_route("GET", "/", self.handle)

        self.loop.create_task(self.__start(self._server, self.port))
        print("Nextcord server is ready!")