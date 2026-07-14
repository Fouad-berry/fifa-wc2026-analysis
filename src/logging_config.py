import logging
from datetime import timedelta

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, ProgressColumn, SpinnerColumn, Task, TextColumn


class ElapsedColumn(ProgressColumn):
    """Custom progress column showing elapsed time as HH:MM:SS."""

    def render(self, task: Task) -> str:
        if task.elapsed is None:
            return ""
        return str(timedelta(seconds=int(task.elapsed)))


def setup_logging(level: int = logging.INFO) -> None:
    """Configure Rich-based logging with tracebacks and markup support."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
        force=True,
    )


_console: Console | None = None


def get_console() -> Console:
    """Return the singleton Rich console instance."""
    global _console
    if _console is None:
        _console = Console()
    return _console


def get_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("\u2022"),
        TextColumn("{task.completed:,}/{task.total:,}"),
        ElapsedColumn(),
        console=get_console(),
    )
