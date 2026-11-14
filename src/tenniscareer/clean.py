"""Clean raw tennisabstract.com match records into a tidy data frame.

Female (WTA) files give each opponent's date of birth (e.g. "19770119"),
so the opponent's age has to be computed. Male (ATP) files already give
the opponent's age at the match (e.g. "22.264202601").
"""

import pandas as pd

DAYS_PER_YEAR = 365.25

# Position of each field we keep inside one raw match record.
FIELDS = {
    "date": 0,
    "tournament": 1,
    "surface": 2,
    "round": 8,
    "result": 4,
    "score": 9,
    "opponent": 11,
    "opponent_birth_or_age": 16,
}


def _records_to_frame(records):
    """Keep only the fields we need from each raw record."""
    rows = [{name: rec[i] for name, i in FIELDS.items()} for rec in records]
    frame = pd.DataFrame(rows, columns=list(FIELDS))
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d")
    return frame


def _age_in_years(dates, birth_dates):
    """Age (in years, with decimals) on `dates` for people born on `birth_dates`."""
    return (dates - birth_dates).dt.days / DAYS_PER_YEAR


def opponent_ages(frame):
    """Opponent age at each match, from either a birth date or an age field."""
    raw = frame["opponent_birth_or_age"].astype(str).str.strip()
    is_birth_date = raw.str.fullmatch(r"\d{8}")
    birth = pd.to_datetime(raw.where(is_birth_date), format="%Y%m%d", errors="coerce")
    from_birth = _age_in_years(frame["date"], birth)
    given_age = pd.to_numeric(raw.where(~is_birth_date), errors="coerce")
    return from_birth.where(is_birth_date, given_age)


def clean_matches(records, birth_date, player_name):
    """Build the cleaned match table used for plotting.

    `age_diff` is opponent age minus player age, so a positive value
    means the opponent was older than the player.
    """
    frame = _records_to_frame(records)
    player_birth = pd.Timestamp(pd.to_datetime(birth_date, format="%Y%m%d"))
    frame["player_age"] = (frame["date"] - player_birth).dt.days / DAYS_PER_YEAR
    frame["opponent_age"] = opponent_ages(frame)
    frame["age_diff"] = frame["opponent_age"] - frame["player_age"]
    frame["result"] = frame["result"].map({"W": "Win", "L": "Loss"})
    frame.insert(0, "player", player_name)
    frame = frame.drop(columns="opponent_birth_or_age")
    return frame.sort_values("date").reset_index(drop=True)