from rich.console import Console
from rich.markdown import Markdown


def print_md(markdown: str):
    console = Console()
    md = Markdown(markdown)
    console.print(md)
