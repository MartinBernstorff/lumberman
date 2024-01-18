import enum
from typing import Annotated

import typer


class Location(str, enum.Enum):
    up = "up"
    top = "top"
    down = "down"
    bottom = "bottom"
    trunk = "trunk"


LocationCLIOption = Annotated[
    Location, typer.Argument(default=None, help="Where to locate the new item.")
]
