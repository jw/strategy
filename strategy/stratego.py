"""The Stratego textual application."""

import logging

from rich.logging import RichHandler
from rich.panel import Panel
from rich.style import StyleType
from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView
from textual.widget import Widget

from strategy.board import Board
from strategy.colour import Colour
from strategy.pieces import Empty, Field, Lake, Piece

FORMAT = "%(message)s"
logging.basicConfig(level="WARNING", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger("stratego")


class StrategyError(Exception):
    """Base strategy exception."""

    pass


class FieldWidget(Widget):
    """The field widget."""

    BLUE = "blue on rgb(51,51,51)"
    RED = "red on rgb(51,51,51)"
    GREEN = "green on rgb(51,51,51)"
    EMPTY = "black on rgb(51,51,51)"

    mouse_over = Reactive(False)

    def __init__(self, field: Field, style: StyleType = "") -> None:
        """Create the field."""
        super().__init__()
        self.field = field
        self.field_style = style

    def render(self) -> Panel:
        """Render the field."""
        if isinstance(self.field, Empty):
            style = self.EMPTY
            name = ""
        elif isinstance(self.field, Lake):
            style = self.GREEN
            name = self.field.name
        elif isinstance(self.field, Piece):
            if self.field.colour == Colour.RED:
                style = self.RED
            else:
                style = self.BLUE
            name = self.field.rich_name
        else:
            raise StrategyError
        return Panel(name, width=15, style=("on purple" if self.mouse_over else style))

    def on_enter(self) -> None:
        """Handle on enter."""
        self.mouse_over = True

    def on_leave(self) -> None:
        """Handle on leave."""
        self.mouse_over = False

    def on_click(self, event: events.Click) -> None:
        """Handle on click."""
        log.info(f"{event=} | {event.button=} | {self}")


class Strategy(GridView):
    """The strategy view."""

    async def on_mount(self) -> None:
        """Create the grid layout."""
        self.board = Board()
        self.board.create_random_pieces(Colour.RED)
        self.board.create_random_pieces(Colour.BLUE)

        self.fields = []
        grid = [[self.board[x, y] for x in range(10)] for y in range(10)]
        for lines in grid:
            for field in lines:
                self.fields.append(FieldWidget(field))

        log.info(self.fields)

        self.grid.set_align("center", "center")

        self.grid.add_column("col", repeat=10)
        self.grid.add_row("row", repeat=10)

        self.grid.place(*self.fields)


class StrategyApp(App):
    """The strategy application."""

    async def on_load(self) -> None:
        """Bind keys."""
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        """Mount the calculator widget."""
        await self.view.dock(Strategy())


def main() -> None:
    """Start the strategy app."""
    StrategyApp.run(log="textual.log", log_verbosity=2)


if __name__ == "__main__":
    main()
