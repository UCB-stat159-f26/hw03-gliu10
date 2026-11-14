"""tenniscareer: tennis career matches from tennisabstract.com, plotted NYT-style."""

from .data import get_career_matches
from .fetch import PlayerNotFoundError
from .plot import plot_age_gap

__all__ = ["get_career_matches", "plot_age_gap", "PlayerNotFoundError"]
__version__ = "0.1.0"