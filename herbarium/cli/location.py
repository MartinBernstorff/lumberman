import enum
from typing import Annotated

import typer


class Location(str, enum.Enum):
    after = "after"
    back = "back"
    before = "before"
    front = "front"


LocationCLIOption = Annotated[Location, typer.Argument(help="Where to locate the new item.")]
