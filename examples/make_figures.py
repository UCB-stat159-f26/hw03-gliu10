"""Regenerate the example figures shown in the README.

Run from the top of the repo (needs internet):
    python examples/make_figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

from tenniscareer import get_career_matches, plot_age_gap  # noqa: E402

OUT_DIR = Path("images")
PLAYERS = {"serena.png": "serena williams", "nadal.png": "Rafael Nadal"}


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for filename, player in PLAYERS.items():
        ax = plot_age_gap(get_career_matches(player))
        ax.figure.savefig(OUT_DIR / filename, dpi=150, bbox_inches="tight")
        plt.close(ax.figure)
        print(f"saved {OUT_DIR / filename}")


if __name__ == "__main__":
    main()