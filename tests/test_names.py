import pytest

from tenniscareer.names import to_player_key


@pytest.mark.parametrize("typed", ["serena williams", "Serena Williams",
                                   "SerenaWilliams", "  serena   williams "])
def test_name_formats_give_same_key(typed):
    assert to_player_key(typed) == "SerenaWilliams"


def test_multi_word_and_punctuation():
    assert to_player_key("juan martin del potro") == "JuanMartinDelPotro"
    assert to_player_key("Felix Auger-Aliassime") == "FelixAugerAliassime"


def test_accents_removed():
    assert to_player_key("Gaël Monfils") == "GaelMonfils"


@pytest.mark.parametrize("bad", ["", "   ", None, 42])
def test_empty_or_non_string_rejected(bad):
    with pytest.raises(ValueError):
        to_player_key(bad)