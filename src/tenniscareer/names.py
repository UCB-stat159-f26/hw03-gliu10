"""Turn a player name typed by a user into the key tennisabstract.com uses."""

import re
import unicodedata


def _strip_accents(text):
    """Remove accents, e.g. 'Gaël' -> 'Gael'."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def to_player_key(player_name):
    """Convert a name like 'serena williams' into 'SerenaWilliams'.

    Each word gets a capital first letter and the rest of the word is
    kept as typed, so 'SerenaWilliams' passes through unchanged.
    Spaces, hyphens, apostrophes and periods are dropped.
    """
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("player_name must be a non-empty string, e.g. 'Serena Williams'")
    words = re.split(r"[^A-Za-z]+", _strip_accents(player_name))
    return "".join(word[0].upper() + word[1:] for word in words if word)