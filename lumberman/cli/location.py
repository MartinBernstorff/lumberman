import enum
from typing import Annotated

import typer


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

    def to_full_location(self) -> "Location":
        if self == Location.to:
            return Location.top
        if self == Location.do:
            return Location.down
        if self == Location.bo:
            return Location.bottom
        if self == Location.tr:
            return Location.trunk
        raise ValueError(f"Unknown location {self}")


LocationCLIOption = Annotated[Location, typer.Argument()]
