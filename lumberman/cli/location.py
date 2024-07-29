import enum
from typing import Annotated

import typer


class FullLocation(str, enum.Enum):
    trunk = "trunk"
    bottom = "bottom"
    top = "top"
    up = "up"
    down = "down"


class Location(str, enum.Enum):
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
            case Location.to | Location.top:
                return FullLocation.top
            case Location.do | Location.down:
                return FullLocation.down
            case Location.bo | Location.bottom:
                return FullLocation.bottom
            case Location.tr | Location.trunk:
                return FullLocation.trunk
            case Location.up:
                return FullLocation.up


LocationCLIOption = Annotated[Location, typer.Argument()]
