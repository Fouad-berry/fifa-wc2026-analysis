"""
viz.py
------
Generate key analysis plots using matplotlib, seaborn, and plotly.
"""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.logging_config import setup_logging
from src.paths import DM_BASE, EXPORTS_DIR, PROCESSED_PATH, PROJECT_ROOT

log = logging.getLogger(__name__)

FIGS_DIR = PROJECT_ROOT / "figures"
sns.set_theme(style="whitegrid")


def _ensure_dir() -> None:
    FIGS_DIR.mkdir(parents=True, exist_ok=True)


def top_scorers_bar(top_n: int = 15) -> None:
    path = EXPORTS_DIR / "top_scorers.csv"
    if not path.exists():
        log.error("top_scorers.csv not found")
        return
    df = pd.read_csv(path).head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(
        df["player_name"] + " (" + df["team"] + ")",
        df["goals"],
        color=sns.color_palette("Blues_r", n_colors=len(df)),
    )
    ax.set_xlabel("Total Goals")
    ax.set_title(f"Top {top_n} Scorers — FIFA WC 2026")
    ax.invert_yaxis()
    for bar, g in zip(bars, df["goals"]):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            str(int(g)),
            va="center",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "top_scorers.png", dpi=150)
    plt.close(fig)
    log.info("Saved figures/top_scorers.png")


def goals_by_stage() -> None:
    path = EXPORTS_DIR / "agg_by_stage.csv"
    if not path.exists():
        log.error("agg_by_stage.csv not found")
        return
    df = pd.read_csv(path).sort_values("stage_order")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sns.barplot(
        data=df,
        x="tournament_stage",
        y="total_goals",
        ax=ax1,
        palette="Blues_d",
        hue="tournament_stage",
        legend=False,
    )
    ax1.set_title("Total Goals by Stage")
    ax1.tick_params(axis="x", rotation=30)

    sns.lineplot(data=df, x="tournament_stage", y="avg_rating", marker="o", ax=ax2, color="crimson")
    ax2.set_title("Avg Player Rating by Stage")
    ax2.tick_params(axis="x", rotation=30)
    ax2.set_ylim(0, 10)

    fig.tight_layout()
    fig.savefig(FIGS_DIR / "goals_by_stage.png", dpi=150)
    plt.close(fig)
    log.info("Saved figures/goals_by_stage.png")


def position_profile() -> None:
    path = EXPORTS_DIR / "agg_by_position.csv"
    if not path.exists():
        log.error("agg_by_position.csv not found")
        return
    df = pd.read_csv(path)
    metrics = ["avg_rating", "avg_goals", "avg_assists", "avg_defensive_index"]
    melted = df.melt(
        id_vars=["position"], value_vars=metrics, var_name="metric", value_name="value"
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=melted, x="position", y="value", hue="metric", ax=ax)
    ax.set_title("Average Performance by Position")
    ax.legend(
        loc="upper right",
        labels=["Rating", "Goals", "Assists", "Def. Index"],
    )
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "position_profile.png", dpi=150)
    plt.close(fig)
    log.info("Saved figures/position_profile.png")


def team_goals(top_n: int = 20) -> None:
    path = DM_BASE / "dm_teams/team_dim.csv"
    if not path.exists():
        log.error("team_dim.csv not found")
        return
    df = pd.read_csv(path).sort_values("total_goals", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = sns.color_palette("viridis", n_colors=len(df))
    ax.bar(df["team"], df["total_goals"], color=colors)
    ax.set_title(f"Top {top_n} Teams by Total Goals")
    ax.set_xlabel("Team")
    ax.set_ylabel("Total Goals")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "team_goals.png", dpi=150)
    plt.close(fig)
    log.info("Saved figures/team_goals.png")


def tournament_heatmap(df: pd.DataFrame | None = None) -> None:
    if df is None:
        path = PROCESSED_PATH
        if not path.exists():
            log.error("Processed file not found")
            return
        df = pd.read_csv(path)
    pivot = df.pivot_table(
        index="tournament_stage",
        columns="position",
        values="player_rating",
        aggfunc="mean",
    )
    order = [
        "Group Stage",
        "Round of 32",
        "Round of 16",
        "Quarter Finals",
        "Semi Finals",
        "Third Place Match",
        "Final",
    ]
    pivot = pivot.reindex([s for s in order if s in pivot.index])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="RdYlGn", ax=ax, linewidths=0.5)
    ax.set_title("Avg Player Rating: Stage x Position")
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "tournament_heatmap.png", dpi=150)
    plt.close(fig)
    log.info("Saved figures/tournament_heatmap.png")


def physical_correlation(df: pd.DataFrame | None = None) -> None:
    if df is None:
        path = PROCESSED_PATH
        if not path.exists():
            log.error("Processed file not found")
            return
        df = pd.read_csv(path)
    cols = [
        "distance_covered_km",
        "sprint_distance_km",
        "top_speed_kmh",
        "stamina_score",
        "accelerations",
        "player_rating",
    ]
    cols = [c for c in cols if c in df.columns]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=ax,
        vmin=-1,
        vmax=1,
        center=0,
        linewidths=0.5,
    )
    ax.set_title("Correlation — Physical Stats & Rating")
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "physical_correlation.png", dpi=150)
    plt.close(fig)
    log.info("Saved figures/physical_correlation.png")


def run_all() -> None:
    _ensure_dir()
    top_scorers_bar()
    goals_by_stage()
    position_profile()
    team_goals()
    if PROCESSED_PATH.exists():
        df = pd.read_csv(PROCESSED_PATH)
        tournament_heatmap(df)
        physical_correlation(df)
    else:
        log.warning("Processed file not found — skipping heatmap and correlation plots")
    print(f"\nAll figures saved to [cyan]{FIGS_DIR}[/]")


if __name__ == "__main__":
    setup_logging()
    run_all()
