import enum
from typing import Annotated

import typer


class FullLocation(str, enum.Enum):
    trunk = "trunk"
    bottom = "bottom"
    top = "top"
    up = "up"
    down = "down"


class StackLocation(str, enum.Enum):
    up = "up"
    top = "top"
    to = "to"
    down = "down"
    do = "do"
    bottom = "bottom"
    bo = "bo"
    trunk = "trunk"
    tr = "tr"

    @property
    def to_full_location(self) -> "FullLocation":
        match self:
            case StackLocation.to | StackLocation.top:
                return FullLocation.top
            case StackLocation.do | StackLocation.down:
                return FullLocation.down
            case StackLocation.bo | StackLocation.bottom:
                return FullLocation.bottom
            case StackLocation.tr | StackLocation.trunk:
                return FullLocation.trunk
            case StackLocation.up:
                return FullLocation.up
            case _:
                raise ValueError(f"Unknown location: {self}")


LocationCLIOption = Annotated[StackLocation, typer.Argument()]
