import logging

import pandas as pd
from scipy import stats

from src.logging_config import get_console, setup_logging
from src.paths import PROCESSED_PATH

log = logging.getLogger(__name__)
console = get_console()

SKEW_CUTOFF = 1.0
KURTOSIS_CUTOFF = 1.0


def describe_distribution(series: pd.Series) -> dict:
    vals = series.dropna()
    if len(vals) < 2:
        return {}

    return {
        "count": len(vals),
        "mean": round(vals.mean(), 3),
        "std": round(vals.std(), 3),
        "min": round(vals.min(), 3),
        "p25": round(vals.quantile(0.25), 3),
        "p50": round(vals.median(), 3),
        "p75": round(vals.quantile(0.75), 3),
        "max": round(vals.max(), 3),
        "skew": round(stats.skew(vals), 3),
        "kurtosis": round(stats.kurtosis(vals, fisher=True), 3),
    }


def run_all() -> None:
    if not PROCESSED_PATH.exists():
        log.error("Processed file not found at %s", PROCESSED_PATH)
        return

    df = pd.read_csv(PROCESSED_PATH, parse_dates=["match_date"])
    numeric_cols = df.select_dtypes(include="number").columns

    console.rule("[bold]DATA PROFILING REPORT[/]")
    console.print(f"Columns profiled: [cyan]{len(numeric_cols)}[/]")
    console.print(f"Rows: [cyan]{len(df):,}[/]")
    console.print()

    for col in sorted(numeric_cols):
        d = describe_distribution(df[col])
        if not d:
            continue

        flags = []
        if abs(d["skew"]) > SKEW_CUTOFF:
            flags.append(f"skewed({d['skew']:+.2f})")
        if abs(d["kurtosis"]) > KURTOSIS_CUTOFF:
            flags.append(f"heavy_tails(kurt={d['kurtosis']:+.2f})")

        flag_str = f"  [yellow]⚠ {' | '.join(flags)}[/]" if flags else ""
        console.print(
            f"  {col:35s}  {d['mean']:>8.3f} ± {d['std']:<8.3f}"
            f"  [{d['min']:>8.3f} – {d['max']:>8.3f}]"
            f"  n={d['count']:>6,}"
            f"{flag_str}"
        )

    console.print()
    log.info("Profiling complete ✓")


if __name__ == "__main__":
    setup_logging()
    run_all()
