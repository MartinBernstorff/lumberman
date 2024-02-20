# Lumberman

[![Open in Dev Container](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)][dev container]
[![PyPI](https://img.shields.io/pypi/v/lumberman.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/lumberman)][pypi status]
[![Roadmap](https://img.shields.io/badge/Board-Roadmap-green)][roadmap]

[dev container]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/MartinBernstorff/lumberman/
[pypi status]: https://pypi.org/project/lumberman/
[documentation]: https://MartinBernstorff.github.io/lumberman/
[roadmap]: https://github.com/users/MartinBernstorff/projects/5

**Lumberman** aims to simplify [stacking](https://stacking.dev/). It's a CLI that helps you:

- 🚀 Tying into your issue tracker and using it to name branches, so you can quickly get to work
- 🗺️ A consistent, carefully curated set of commands and constantly giving you feedback, so you can navigate with confidence
- 🧠 Strategically synchronising local and remote when it makes sense, so you have to keep less state in your head the amount of state you have to keep in your head by 

## Installation
```bash
pipx install lumberman
```

## Usage
To see inline documentation:
```bash
lumberman
```

Or the alias:
```bash
lm
```

<img align="right" src="https://github.com/MartinBernstorff/lumberman/assets/8526086/11effdd6-39aa-4f05-8eba-2ea730278e10"/>

## Case study

Let's look at a case! Say you're working on branch A, and you notice you can add an optimisation by making a small configuration change. Previously, you would have to:

1. Switch from branch A to main
1. Pull main to ensure you're aligned with remote
1. Create a new branch from main
1. Name the branch (Patch)
1. Commit changes
1. Push
1. Create a PR
1. Switch to branch A
1. Merge the Patch-cfg branch into branch A

But with lumberman:

1. lm insert bottom
1. Commit changes
1. lm sync
1. lm top

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
