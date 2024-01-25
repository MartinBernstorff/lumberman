# `lumberman`

All commands are registered as [sh]orthand. You can call the command as 'lm sh' or 'lumberman shorthand'.

**Usage**:

```console
$ lumberman [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

* `[bo]ttom`: Go to the bottom of the stack.
* `[ch]heckout`: Prompt to checkout an item in the stack.
* `[d]elete`: Prompt to delete an item.
* `[do]wn`: Go to the item below the current one.
* `[f]ork`: Fork into a new stack and add an item.
* `[i]nsert`: Prompt to create a new item on the current...
* `[l]og`: Print the current stack status.
* `[m]ove`: Move the current item to a new location in...
* `[n]ew`: Start a new stack on top of trunk.
* `[s]ync`: Synchronize all state, ensuring the stack...
* `[to]p`: Go to the top of the stack.
* `[up]`: Go to the item above the current one.
* `bo`: Go to the bottom of the stack.
* `bottom`: Go to the bottom of the stack.
* `ch`: Prompt to checkout an item in the stack.
* `chheckout`: Prompt to checkout an item in the stack.
* `d`: Prompt to delete an item.
* `delete`: Prompt to delete an item.
* `do`: Go to the item below the current one.
* `down`: Go to the item below the current one.
* `f`: Fork into a new stack and add an item.
* `fork`: Fork into a new stack and add an item.
* `i`: Prompt to create a new item on the current...
* `insert`: Prompt to create a new item on the current...
* `l`: Print the current stack status.
* `log`: Print the current stack status.
* `m`: Move the current item to a new location in...
* `move`: Move the current item to a new location in...
* `n`: Start a new stack on top of trunk.
* `new`: Start a new stack on top of trunk.
* `s`: Synchronize all state, ensuring the stack...
* `sync`: Synchronize all state, ensuring the stack...
* `to`: Go to the top of the stack.
* `top`: Go to the top of the stack.
* `up`: Go to the item above the current one.

## `lumberman [bo]ttom`

Go to the bottom of the stack.

**Usage**:

```console
$ lumberman [bo]ttom [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [ch]heckout`

Prompt to checkout an item in the stack.

**Usage**:

```console
$ lumberman [ch]heckout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman [d]elete`

Prompt to delete an item.

**Usage**:

```console
$ lumberman [d]elete [OPTIONS]
```

**Options**:

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

* `--location [up|top|down|bottom|trunk]`: [default: Location.bottom]
* `--help`: Show this message and exit.

## `lumberman [i]nsert`

Prompt to create a new item on the current stack. Defaults to creating an item in between the current item and the next item.

**Usage**:

```console
$ lumberman [i]nsert [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom|trunk]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman [l]og`

Print the current stack status.

**Usage**:

```console
$ lumberman [l]og [OPTIONS]
```

**Options**:

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

## `lumberman ch`

Prompt to checkout an item in the stack.

**Usage**:

```console
$ lumberman ch [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman chheckout`

Prompt to checkout an item in the stack.

**Usage**:

```console
$ lumberman chheckout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman d`

Prompt to delete an item.

**Usage**:

```console
$ lumberman d [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman delete`

Prompt to delete an item.

**Usage**:

```console
$ lumberman delete [OPTIONS]
```

**Options**:

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

* `--location [up|top|down|bottom|trunk]`: [default: Location.bottom]
* `--help`: Show this message and exit.

## `lumberman fork`

Fork into a new stack and add an item. Defaults to forking from the first item in the current stack.

**Usage**:

```console
$ lumberman fork [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom|trunk]`: [default: Location.bottom]
* `--help`: Show this message and exit.

## `lumberman i`

Prompt to create a new item on the current stack. Defaults to creating an item in between the current item and the next item.

**Usage**:

```console
$ lumberman i [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom|trunk]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman insert`

Prompt to create a new item on the current stack. Defaults to creating an item in between the current item and the next item.

**Usage**:

```console
$ lumberman insert [OPTIONS]
```

**Options**:

* `--location [up|top|down|bottom|trunk]`: [default: Location.up]
* `--help`: Show this message and exit.

## `lumberman l`

Print the current stack status.

**Usage**:

```console
$ lumberman l [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lumberman log`

Print the current stack status.

**Usage**:

```console
$ lumberman log [OPTIONS]
```

**Options**:

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
