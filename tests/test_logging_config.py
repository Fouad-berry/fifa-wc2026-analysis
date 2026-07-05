import logging

from rich.progress import Progress

from src.logging_config import ElapsedColumn, get_console, get_progress, setup_logging


def test_setup_logging():
    setup_logging(logging.DEBUG)
    logger = logging.getLogger(__name__)
    assert logger.isEnabledFor(logging.DEBUG)


def test_get_console():
    console = get_console()
    assert console is not None
    assert get_console() is console


def test_get_progress():
    progress = get_progress()
    assert isinstance(progress, Progress)
    assert len(progress.columns) == 7


def test_elapsed_column_type():
    col = ElapsedColumn()
    assert col is not None
