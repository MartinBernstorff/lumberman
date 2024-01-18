import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable

import typer

from lumberman.cli import manipulation as man
from lumberman.cli import navigation as nav

app = typer.Typer(
    no_args_is_help=True,
    add_help_option=False,
    add_completion=False,
    help="All commands are registered as [sh]orthand. You can call the command as 'sh' or 'shorthand'.",
)


@dataclass(frozen=True)
class Command:
    name: str
    fn: Callable[[], None]


@dataclass(frozen=True)
class CommandSection:
    name: str
    commands: Sequence[Command]


commands = [
    CommandSection(
        name="Nav: End of stack",
        commands=[Command(name="[bo]ottom", fn=nav.bottom), Command(name="[to]p", fn=nav.top)],
    ),
    CommandSection(
        name="Nav: Stepwise",
        commands=[Command(name="[do]wn", fn=nav.down), Command(name="[up]", fn=nav.up)],
    ),
    CommandSection(name="Orientation", commands=[Command(name="[st]atus", fn=nav.status)]),
    CommandSection(
        name="Manipulation",
        commands=[
            Command(name="[a]dd", fn=man.add),
            Command(name="[d]elete", fn=man.add),
            Command(name="[f]ork", fn=man.fork),
            Command(name="[m]ove", fn=man.move),
            Command(name="[n]ew", fn=man.new),
            Command(name="[s]ync", fn=man.sync),
        ],
    ),
]

shorthands: set[str] = set()

for section in commands:
    for command in section.commands:
        app.command(name=command.name, rich_help_panel=section.name)(command.fn)

        command_shorthand = re.findall(r"\[(.*?)\]", command.name)[0]

        if command_shorthand in shorthands:
            raise ValueError(f"Duplicate shorthand '{command_shorthand}'")

        shorthands.add(command_shorthand)
        app.command(name=command_shorthand, hidden=True)(command.fn)

        command_full = command.name.replace("[", "").replace("]", "")
        app.command(name=command_full, hidden=True)(command.fn)


if __name__ == "__main__":
    app()
