import enum
from typing import Annotated

import typer


class Location(str, enum.Enum):
    up = "up"
    top = "top"
    down = "down"
    bottom = "bottom"


LocationCLIOption = Annotated[Location, typer.Argument(help="Where to locate the new item.")]
