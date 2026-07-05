from src.cli_runner import (
    all_cmds,
    datamarts,
    ingest,
    metrics,
    pipeline,
    profile,
    sql,
    transform,
    visualize,
)


def test_dispatch_all_keys_present():
    """Every key in the fire.Fire() dispatch dict has a matching function."""
    dispatch = {
        "ingest": ingest,
        "transform": transform,
        "datamarts": datamarts,
        "metrics": metrics,
        "visualize": visualize,
        "profile": profile,
        "sql": sql,
        "pipeline": pipeline,
        "all": all_cmds,
    }
    for name, func in dispatch.items():
        assert callable(func), f"{name} is not callable"
    assert len(dispatch) == 9
