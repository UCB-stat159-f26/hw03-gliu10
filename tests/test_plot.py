import matplotlib

matplotlib.use("Agg")  # draw without opening a window

import pytest  # noqa: E402

from tenniscareer import plot_age_gap  # noqa: E402
from tenniscareer.clean import clean_matches  # noqa: E402
from tenniscareer.parse import extract_js_array  # noqa: E402


@pytest.fixture
def male(male_career_js):
    return clean_matches(extract_js_array(male_career_js), "19860603", "Rafael Nadal")


def test_one_scatter_per_result(male):
    ax = plot_age_gap(male)
    assert [c.get_label() for c in ax.collections] == ["Win", "Loss"]
    assert len(ax.collections[0].get_offsets()) == 1
    assert len(ax.collections[1].get_offsets()) == 2


def test_labels(male):
    ax = plot_age_gap(male)
    assert "Rafael Nadal" in ax.get_xlabel()
    assert "Opponent" in ax.get_ylabel()