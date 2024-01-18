from .cli.subprocess_utils import interactive_cmd


def test_generate_docs():
    interactive_cmd("typer lumberman/__main__.py utils docs --name lumberman --output DOCS.md")
