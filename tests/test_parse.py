import pytest

from tenniscareer.parse import extract_birth_date, extract_full_name, extract_js_array


def test_female_array(female_career_js):
    records = extract_js_array(female_career_js)
    assert len(records) == 3
    assert records[0][0] == "19951030"
    assert records[0][11] == "Anne Miller"
    assert records[0][16] == "19770119"


def test_male_array(male_career_js):
    records = extract_js_array(male_career_js)
    assert len(records) == 3
    assert records[2][11] == "Israel Matos Gil"
    assert records[2][16] == "18.7597535934"


def test_missing_variable_raises():
    with pytest.raises(ValueError, match="morematchmx"):
        extract_js_array("var somethingelse = [];")


def test_profile_fields(female_profile_js, male_profile_js):
    assert extract_birth_date(female_profile_js) == "19810926"
    assert extract_birth_date(male_profile_js) == "19860603"
    assert extract_full_name(male_profile_js) == "Rafael Nadal"


def test_profile_fields_missing():
    assert extract_birth_date("") is None
    assert extract_full_name("") is None