import pytest

from models.elo import ELOSystem


@pytest.mark.parametrize("rating_1, rating_2, expected", [
    (1000, 1000, 0.5),
    (1200, 1000, 0.7597),
    (1000, 1200, 0.2402),
])
def test_expected_score(rating_1, rating_2, expected):
    assert abs(ELOSystem.expected_score(rating_1, rating_2) - expected) < 0.0001

def test_rating_update():
    player_1, player_2 = ELOSystem.update_rating(1000, 1000, 1)
    assert player_1 == 1016
    assert player_2 == 984