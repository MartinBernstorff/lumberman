import typer

from .cli import manipulation as man
from .cli import navigation as nav

app = typer.Typer(no_args_is_help=True, add_help_option=False, add_completion=False, help="Test")

# Navigation
end_of_queue_help_panel_str = "End of queue navigation"
app.command(rich_help_panel=end_of_queue_help_panel_str)(nav.front)
app.command(rich_help_panel=end_of_queue_help_panel_str)(nav.back)

navigation_help_panel_str = "Stepwise navigation"
app.command(rich_help_panel=navigation_help_panel_str)(nav.before)
app.command(rich_help_panel=navigation_help_panel_str)(nav.after)

orientation_help_panel_str = "Orientation"
app.command(rich_help_panel=orientation_help_panel_str)(nav.status)

# Manipulation
manipulation_help_panel_str = "Manipulation"
app.command(rich_help_panel=manipulation_help_panel_str)(man.add)
app.command(name="a", hidden=True)(man.add)

app.command(name="fo", hidden=True)(man.fork)
app.command(rich_help_panel=manipulation_help_panel_str)(man.fork)

app.command(rich_help_panel=manipulation_help_panel_str)(man.new)
app.command(rich_help_panel=manipulation_help_panel_str)(man.sync)

if __name__ == "__main__":
    app()
