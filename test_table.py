import pytest
from table import Table

def test_win_percentages_01():
    """
    first test to make sure it works
    """
    poker = Table(2)
    assert len(poker.deck.cards) == 52

    poker.set_hole_cards(1, ['As', 'Ad'])
    assert len(poker.deck.cards) == 50

    poker.set_hole_cards(2, ['Kh', 'Kc'])
    assert len(poker.deck.cards) == 48

    poker.flop(['Js', '6c', '9h'])
    assert len(poker.deck.cards) == 45

    odds = poker.calculate()
    assert odds[0] == pytest.approx(.9000, abs=1e-3)
    assert odds[1] == pytest.approx(.1000, abs=1e-3)

    poker.turn('9d')
    assert len(poker.deck.cards) == 44

    odds = poker.calculate()
    assert odds[0] == pytest.approx(.9545, abs=1e-3)
    assert odds[1] == pytest.approx(.0455, abs=1e-3)

    poker.river('Kd')
    assert len(poker.deck.cards) == 43

    odds = poker.calculate()
    assert odds[0] == 0
    assert odds[1] == 1

def test_win_percentages_02():
    """
    check folds
    """

    poker = Table(6)
    assert len(poker.deck.cards) == 52

    poker.set_hole_cards(1, ['3s', '9h'])
    assert len(poker.deck.cards) == 50

    poker.set_hole_cards(2, ['9d', '8c'])
    assert len(poker.deck.cards) == 48

    poker.set_hole_cards(3, ['Qs', '2c'])
    assert len(poker.deck.cards) == 46

    poker.set_hole_cards(4, ['4s', '4d'])
    assert len(poker.deck.cards) == 44

    poker.set_hole_cards(5, ['Qh', '9c'])
    assert len(poker.deck.cards) == 42

    poker.set_hole_cards(6, ['Jd', 'Kd'])
    assert len(poker.deck.cards) == 40

    poker.fold(1)
    poker.fold(3)

    poker.flop(['7d', 'Th', '4c'])
    assert len(poker.deck.cards) == 37

    odds = poker.calculate()
    assert odds[0] == 0
    assert odds[1] == pytest.approx(.2072, abs=1e-3)
    assert odds[2] == 0
    assert odds[3] == pytest.approx(.6997, abs=1e-3)
    assert odds[4] == pytest.approx(.0270, abs=1e-3)
    assert odds[5] == pytest.approx(.0495, abs=1e-3)

    poker.fold(5)

    odds = poker.calculate()
    assert odds[0] == 0
    assert odds[1] == pytest.approx(.2508, abs=1e-3)
    assert odds[2] == 0
    assert odds[3] == pytest.approx(.6997, abs=1e-3)
    assert odds[4] == 0
    assert odds[5] == pytest.approx(.0495, abs=1e-3)

    poker.turn('2d')
    assert len(poker.deck.cards) == 36

    odds = poker.calculate()
    assert odds[0] == 0
    assert odds[1] == pytest.approx(.1667, abs=1e-3)
    assert odds[2] == 0
    assert odds[3] == pytest.approx(.6667, abs=1e-3)
    assert odds[4] == 0
    assert odds[5] == pytest.approx(.1667, abs=1e-3)
