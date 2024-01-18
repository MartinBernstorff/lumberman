import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable

import typer

from herbarium.cli import manipulation as man
from herbarium.cli import navigation as nav

app = typer.Typer(
    no_args_is_help=True,
    add_help_option=False,
    add_completion=False,
    help="All commands are registered as [sh]orthand. You can call the command as 'sh' or 'shorthand'",
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
        name="End of queue navigation",
        commands=[Command(name="[fr]ont", fn=nav.front), Command(name="[ba]ck", fn=nav.back)],
    ),
    CommandSection(
        name="Stepwise navigation",
        commands=[Command(name="[be]efore", fn=nav.before), Command(name="[af]ter", fn=nav.after)],
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
