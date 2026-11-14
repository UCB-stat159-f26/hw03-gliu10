"""Download raw files from tennisabstract.com (the only module that uses the network)."""

from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = "https://www.tennisabstract.com/jsmatches/"
HEADERS = {"User-Agent": "Mozilla/5.0 (tenniscareer Python package)"}


class PlayerNotFoundError(ValueError):
    """Raised when tennisabstract.com has no data for the requested player."""


def download_text(url):
    """Return the text at `url`, or None if the server answers 404."""
    try:
        with urlopen(Request(url, headers=HEADERS), timeout=30) as response:
            return response.read().decode("utf-8")
    except HTTPError as err:
        if err.code == 404:
            return None
        raise


def fetch_player_files(player_key):
    """Download `<key>Career.js` (matches) and `<key>.js` (profile, incl. birth date)."""
    career_js = download_text(f"{BASE_URL}{player_key}Career.js")
    if career_js is None:
        raise PlayerNotFoundError(
            f"No career data found on tennisabstract.com for '{player_key}'. "
            "Check the spelling and use the player's full name, e.g. 'Serena Williams'."
        )
    profile_js = download_text(f"{BASE_URL}{player_key}.js") or ""
    return career_js, profile_js