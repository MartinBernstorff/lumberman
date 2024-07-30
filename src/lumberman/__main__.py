import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import typer

from lumberman.cli import manipulation as man
from lumberman.cli import navigation as nav
from lumberman.cli.config import MANAGER
from lumberman.stack.manipulator import StackManager

if TYPE_CHECKING:
    from collections.abc import Sequence

app = typer.Typer(
    name="[l]umber[m]an",
    no_args_is_help=True,
    add_help_option=False,
    add_completion=False,
    help="All commands are registered as [sh]orthand. You can call the command as 'lm sh' or 'lumberman shorthand'.",
)


@dataclass(frozen=True)
class Command:
    name: str
    fn: Callable[[], None]


@dataclass(frozen=True)
class CommandSection:
    name: str
    commands: "Sequence[Command]"


if __name__ == "__main__":
    # If managing changes as a stack
    stack_commands = [
        CommandSection(
            name="Navigation",
            commands=[
                Command(name="[ch]heckout", fn=nav.checkout),
                Command(name="[bo]ttom", fn=nav.bottom),
                Command(name="[to]p", fn=nav.top),
                Command(name="[do]wn", fn=nav.down),
                Command(name="[up]", fn=nav.up),
            ],
        ),
        CommandSection(name="Orientation", commands=[Command(name="[l]og", fn=nav.log)]),
        CommandSection(
            name="Manipulation",
            commands=[
                Command(name="[i]nsert", fn=man.insert),
                Command(name="[j]ab", fn=man.jab),
                Command(name="[d]elete", fn=man.delete),
                Command(name="[f]ork", fn=man.fork),
                Command(name="[m]ove", fn=man.move),
                Command(name="[n]ew", fn=man.new),
                Command(name="[s]ync", fn=man.sync),
            ],
        ),
    ]

    # In case a stacker is not set
    change_manager_commands = [
        CommandSection(
            name="Change Manager",
            commands=[Command(name="[i]nsert", fn=man.insert), Command(name="[s]ync", fn=man.sync)],
        )
    ]

    commands = stack_commands if isinstance(MANAGER, StackManager) else change_manager_commands  # type: ignore

    shorthands: set[str] = set()

    # Add the commands and shorthands to the app
    for section in stack_commands:
        for command in section.commands:
            # Add the combined command, e.g. [i]nsert
            app.command(name=command.name, rich_help_panel=section.name)(command.fn)

            # Handle shorthand, e.g. i
            command_shorthand = re.findall(r"\[(.*?)\]", command.name)[0]
            if command_shorthand in shorthands:
                raise ValueError(f"Duplicate shorthand '{command_shorthand}'")

            shorthands.add(command_shorthand)
            app.command(name=command_shorthand, hidden=True)(command.fn)

            # Add the full command, e.g. insert
            command_full = command.name.replace("[", "").replace("]", "")
            app.command(name=command_full, hidden=True)(command.fn)
    app()
