# Lumberman

[![Open in Dev Container](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)][dev container]
[![PyPI](https://img.shields.io/pypi/v/lumberman.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/lumberman)][pypi status]
[![Tests](https://github.com/MartinBernstorff/lumberman/actions/workflows/tests.yml/badge.svg)][tests]
[![Roadmap](https://img.shields.io/badge/Board-Roadmap-green)][roadmap]

[dev container]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/lumberman/
[pypi status]: https://pypi.org/project/lumberman/
[documentation]: https://MartinBernstorff.github.io/lumberman/
[tests]: https://github.com/MartinBernstorff/lumberman/actions?workflow=Tests
[roadmap]: https://github.com/users/MartinBernstorff/projects/5


<!-- start short-description -->

TODO: Add a short description of the project

<!-- end short-description -->
## Installation
```bash
pip install lumberman
```
## Usage

TODO: Add minimal usage example

### Setting up a development environment
#### Devcontainer
1. Install [Orbstack](https://orbstack.dev/) or Docker Desktop. Make sure to complete the full install process before continuing.
2. If not installed, install VSCode
3. Press this [link](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/lumberman/)
4. Complete the setup process
5. Done! Easy as that.

# 💬 Where to ask questions

| Type                           |                        |
| ------------------------------ | ---------------------- |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |

[github issue tracker]: https://github.com/MartinBernstorff/lumberman/issues
[github discussions]: https://github.com/MartinBernstorff/lumberman/discussions

# Documentation
# `lumberman`

All commands are registered as [sh]orthand. You can call the command as 'sh' or 'shorthand'.

**Usage**:

```console
$ lumberman [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

* `[a]dd`: Add a new item to the current stack.
* `[bo]ottom`: Go to the bottom of the stack.
* `[d]elete`: Add a new item to the current stack.
* `[do]wn`: Go to the item below the current one.
* `[f]ork`: Fork into a new stack and add an item.
* `[m]ove`: Move the current item to a new location in the stack.
* `[n]ew`: Start a new stack on top of trunk.
* `[s]ync`: Synchronize all state.
* `[st]atus`: Print the current stack status.
* `[to]p`: Go to the top of the stack.
* `[up]`: Go to the item above the current one.

## `lumberman [a]dd`

Add a new item to the current stack. Defaults to adding an item in between the current item and the next item.

**Usage**:

```console
$ lumberman [a]dd [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman [bo]ottom`

Go to the bottom of the stack.

**Usage**:

```console
$ lumberman [bo]ottom [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [d]elete`

Add a new item to the current stack. Defaults to adding an item in between the current item and the next item.

**Usage**:

```console
$ lumberman [d]elete [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman [do]wn`

Go to the item below the current one.

**Usage**:

```console
$ lumberman [do]wn [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [f]ork`

Fork into a new stack and add an item. Defaults to forking from the first item in the current stack.

**Usage**:

```console
$ lumberman [f]ork [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.bottom]
* `--help`: Show this message and exit.

## `lumberman [m]ove`

Move the current item to a new location in the stack.

**Usage**:

```console
$ lumberman [m]ove [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [n]ew`

Start a new stack on top of trunk.

**Usage**:

```console
$ lumberman [n]ew [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [s]ync`

Synchronize all state, ensuring the stack is internally in sync, and in sync with the remote. Creates PRs if needed.

**Usage**:

```console
$ lumberman [s]ync [OPTIONS]
```

**Options**:

* `--automerge / --no-automerge`: [default: no-automerge]
* `--draft / --no-draft`: [default: no-draft]
* `--squash / --no-squash`: [default: no-squash]
* `--help`: Show this message and exit.

## `lumberman [st]atus`

Print the current stack status.

**Usage**:

```console
$ lumberman [st]atus [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [to]p`

Go to the top of the stack.

**Usage**:

```console
$ lumberman [to]p [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [up]`

Go to the item above the current one.

**Usage**:

```console
$ lumberman [up] [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman a`

Add a new item to the current stack. Defaults to adding an item in between the current item and the next item.

**Usage**:

```console
$ lumberman a [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman add`

Add a new item to the current stack. Defaults to adding an item in between the current item and the next item.

**Usage**:

```console
$ lumberman add [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman bo`

Go to the bottom of the stack.

**Usage**:

```console
$ lumberman bo [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman bottom`

Go to the bottom of the stack.

**Usage**:

```console
$ lumberman bottom [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman d`

Add a new item to the current stack. Defaults to adding an item in between the current item and the next item.

**Usage**:

```console
$ lumberman d [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman delete`

Add a new item to the current stack. Defaults to adding an item in between the current item and the next item.

**Usage**:

```console
$ lumberman delete [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman do`

Go to the item below the current one.

**Usage**:

```console
$ lumberman do [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman down`

Go to the item below the current one.

**Usage**:

```console
$ lumberman down [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman f`

Fork into a new stack and add an item. Defaults to forking from the first item in the current stack.

**Usage**:

```console
$ lumberman f [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.bottom]
* `--help`: Show this message and exit.

## `lumberman fork`

Fork into a new stack and add an item. Defaults to forking from the first item in the current stack.

**Usage**:

```console
$ lumberman fork [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom]`: [default: Location.bottom]
* `--help`: Show this message and exit.

## `lumberman m`

Move the current item to a new location in the stack.

**Usage**:

```console
$ lumberman m [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman move`

Move the current item to a new location in the stack.

**Usage**:

```console
$ lumberman move [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman n`

Start a new stack on top of trunk.

**Usage**:

```console
$ lumberman n [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman new`

Start a new stack on top of trunk.

**Usage**:

```console
$ lumberman new [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman s`

Synchronize all state, ensuring the stack is internally in sync, and in sync with the remote. Creates PRs if needed.

**Usage**:

```console
$ lumberman s [OPTIONS]
```

**Options**:

* `--automerge / --no-automerge`: [default: no-automerge]
* `--draft / --no-draft`: [default: no-draft]
* `--squash / --no-squash`: [default: no-squash]
* `--help`: Show this message and exit.

## `lumberman st`

Print the current stack status.

**Usage**:

```console
$ lumberman st [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman status`

Print the current stack status.

**Usage**:

```console
$ lumberman status [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman sync`

Synchronize all state, ensuring the stack is internally in sync, and in sync with the remote. Creates PRs if needed.

**Usage**:

```console
$ lumberman sync [OPTIONS]
```

**Options**:

* `--automerge / --no-automerge`: [default: no-automerge]
* `--draft / --no-draft`: [default: no-draft]
* `--squash / --no-squash`: [default: no-squash]
* `--help`: Show this message and exit.

## `lumberman to`

Go to the top of the stack.

**Usage**:

```console
$ lumberman to [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman top`

Go to the top of the stack.

**Usage**:

```console
$ lumberman top [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman up`

Go to the item above the current one.

**Usage**:

```console
$ lumberman up [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
