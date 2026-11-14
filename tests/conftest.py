"""Shared test helpers: load the mockup JS files from tests/data/."""

from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


def read_mockup(filename):
    return (DATA_DIR / filename).read_text()


@pytest.fixture
def female_career_js():
    return read_mockup("FemalePlayerCareer.JS")


@pytest.fixture
def male_career_js():
    return read_mockup("MalePlayerCareer.JS")


@pytest.fixture
def female_profile_js():
    return read_mockup("FemalePlayerProfile.js")


@pytest.fixture
def male_profile_js():
    return read_mockup("MalePlayerProfile.js")