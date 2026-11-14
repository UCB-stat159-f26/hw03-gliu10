"""tenniscareer: tennis career matches from tennisabstract.com, plotted NYT-style."""

from .data import get_career_matches
from .fetch import PlayerNotFoundError

__all__ = ["get_career_matches", "PlayerNotFoundError"]
__version__ = "0.1.0"