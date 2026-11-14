import pytest

from tenniscareer.clean import clean_matches
from tenniscareer.parse import extract_js_array

EXPECTED_COLUMNS = ["player", "date", "tournament", "surface", "round", "result",
                    "score", "opponent", "player_age", "opponent_age", "age_diff"]


@pytest.fixture
def female(female_career_js):
    return clean_matches(extract_js_array(female_career_js), "19810926", "Serena Williams")


@pytest.fixture
def male(male_career_js):
    return clean_matches(extract_js_array(male_career_js), "19860603", "Rafael Nadal")


def test_columns(female, male):
    assert list(female.columns) == EXPECTED_COLUMNS
    assert list(male.columns) == EXPECTED_COLUMNS


def test_female_ages_from_birth_dates(female):
    first = female.iloc[0]  # 1995-10-30 vs Anne Miller (born 1977-01-19)
    assert first["player_age"] == pytest.approx(14.09, abs=0.01)
    assert first["opponent_age"] == pytest.approx(18.78, abs=0.01)
    assert first["age_diff"] == pytest.approx(4.69, abs=0.01)


def test_male_ages_taken_as_given(male):
    platel = male[male["opponent"] == "Guillermo Platel"].iloc[0]
    assert platel["opponent_age"] == pytest.approx(22.264202601)
    assert platel["player_age"] == pytest.approx(15.27, abs=0.01)


def test_results_and_order(female, male):
    assert set(female["result"]) == {"Loss"}
    assert sorted(male["result"]) == ["Loss", "Loss", "Win"]
    assert male["date"].is_monotonic_increasing


def test_missing_opponent_age_is_nan(male_career_js):
    records = extract_js_array(male_career_js)
    records[0][16] = ""
    cleaned = clean_matches(records, "19860603", "Rafael Nadal")
    assert cleaned["age_diff"].isna().sum() == 1