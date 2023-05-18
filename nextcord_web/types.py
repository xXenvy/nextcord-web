from typing import List, Union, Literal
from nextcord import Client, Guild


Snowflake = Union[str, int]
SnowflakeList = List[Snowflake]
API_VERSION = Literal[9, 10]