import enum
from typing import Annotated

import typer


class Location(str, enum.Enum):
    front = "front"
    before = "before"
    after = "after"
    back = "back"


LocationCLIOption = Annotated[Location, typer.Argument(help="Where to locate the new item.")]
