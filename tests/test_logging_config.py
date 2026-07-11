import logging
from unittest.mock import MagicMock

from rich.progress import Progress, Task

from src.logging_config import ElapsedColumn, get_console, get_progress, setup_logging


def test_setup_logging() -> None:
    setup_logging(logging.DEBUG)
    logger = logging.getLogger(__name__)
    assert logger.isEnabledFor(logging.DEBUG)


def test_get_console() -> None:
    console = get_console()
    assert console is not None
    assert get_console() is console


def test_get_progress() -> None:
    progress = get_progress()
    assert isinstance(progress, Progress)
    assert len(progress.columns) == 7


def test_elapsed_column_type() -> None:
    col = ElapsedColumn()
    assert col is not None


def test_elapsed_column_render_empty_when_no_elapsed() -> None:
    col = ElapsedColumn()
    task = MagicMock(spec=Task)
    task.elapsed = None
    result = col.render(task)
    assert result == ""


def test_elapsed_column_render_returns_seconds() -> None:
    col = ElapsedColumn()
    task = MagicMock(spec=Task)
    task.elapsed = 3661.5
    result = col.render(task)
    assert result == "1:01:01"
