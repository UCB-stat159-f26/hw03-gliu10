"""Tests for get_career_matches(). The network is replaced by the mockups,
so these tests never contact tennisabstract.com."""

import pytest

import tenniscareer.fetch as fetch_module
from tenniscareer import PlayerNotFoundError, get_career_matches


def fake_downloader(files):
    """Return a stand-in for download_text() that serves `files` by URL suffix."""
    def download(url):
        for suffix, text in files.items():
            if url.endswith("/" + suffix):
                return text
        return None  # behaves like a 404
    return download


def test_female_player(monkeypatch, female_career_js, female_profile_js):
    monkeypatch.setattr(fetch_module, "download_text", fake_downloader({
        "SerenaWilliamsCareer.js": female_career_js,
        "SerenaWilliams.js": female_profile_js}))
    matches = get_career_matches("serena williams")
    assert len(matches) == 3
    assert matches["player"].iloc[0] == "Serena Williams"


def test_male_player(monkeypatch, male_career_js, male_profile_js):
    monkeypatch.setattr(fetch_module, "download_text", fake_downloader({
        "RafaelNadalCareer.js": male_career_js,
        "RafaelNadal.js": male_profile_js}))
    assert get_career_matches("Rafael Nadal")["age_diff"].notna().all()


def test_unknown_player(monkeypatch):
    monkeypatch.setattr(fetch_module, "download_text", fake_downloader({}))
    with pytest.raises(PlayerNotFoundError, match="GastonSanchez"):
        get_career_matches("GastonSanchez")


def test_missing_birth_date_can_be_supplied(monkeypatch, female_career_js):
    monkeypatch.setattr(fetch_module, "download_text", fake_downloader({
        "SerenaWilliamsCareer.js": female_career_js}))
    with pytest.raises(PlayerNotFoundError, match="birth date"):
        get_career_matches("Serena Williams")
    matches = get_career_matches("Serena Williams", birth_date="19810926")
    assert matches["player_age"].iloc[0] == pytest.approx(14.09, abs=0.01)