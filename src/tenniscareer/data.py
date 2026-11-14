"""Public function that returns a player's cleaned career matches."""

from .clean import clean_matches
from .fetch import PlayerNotFoundError, fetch_player_files
from .names import to_player_key
from .parse import extract_birth_date, extract_full_name, extract_js_array


def get_career_matches(player_name, birth_date=None):
    """Download and clean a player's career matches from tennisabstract.com.

    player_name: e.g. "serena williams", "Serena Williams" or "SerenaWilliams".
    birth_date:  optional "yyyymmdd" string; only needed if tennisabstract.com
                 does not list the player's birth date.

    Returns a pandas DataFrame with one row per match, including the
    player's age, the opponent's age, `age_diff` and the result.
    """
    player_key = to_player_key(player_name)
    career_js, profile_js = fetch_player_files(player_key)
    birth_date = birth_date or extract_birth_date(profile_js)
    if birth_date is None:
        raise PlayerNotFoundError(
            f"Found matches for '{player_key}' but no birth date; "
            "pass it yourself, e.g. birth_date='19810926'."
        )
    display_name = extract_full_name(profile_js) or player_name
    return clean_matches(extract_js_array(career_js), birth_date, display_name)