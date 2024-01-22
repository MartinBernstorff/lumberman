import enum


class Location(str, enum.Enum):
    up = "up"
    top = "top"
    down = "down"
    bottom = "bottom"
    trunk = "trunk"


LocationCLIOption = Location
