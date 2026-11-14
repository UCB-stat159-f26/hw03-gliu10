"""Public function that draws the NYT-style age-gap scatter plot."""

import matplotlib.pyplot as plt

COLORS = {"Win": "#2b6cb0", "Loss": "#e8590c"}


def _style_axes(ax, player):
    """Axis labels, zero line and title for the age-gap plot."""
    ax.axhline(0, color="gray", linewidth=0.8, zorder=0)
    ax.set_xlabel(f"{player}'s age")
    ax.set_ylabel("Opponent's age minus player's age (years)")
    ax.set_title(f"{player}: opponents older (above 0) or younger (below 0)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")


def plot_age_gap(matches, ax=None):
    """Scatter plot of player age (x) vs. opponent age difference (y).

    matches: the DataFrame returned by get_career_matches().
    ax:      optional matplotlib Axes to draw on.
    Each point is a match, colored by win or loss. Returns the Axes.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    for result, color in COLORS.items():
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_diff"], s=14,
                   alpha=0.6, color=color, label=result, edgecolors="none")
    player = matches["player"].iloc[0] if len(matches) else "Player"
    _style_axes(ax, player)
    return ax