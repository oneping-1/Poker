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

def test_win_percentages_03():
    """
    checks tie logics
    """
    poker = Table(2)
    assert len(poker.deck.cards) == 52

    poker.set_hole_cards(1, ['2s', '7s'])
    poker.set_hole_cards(2, ['2c', '7c'])
    assert len(poker.deck.cards) == 48

    poker.flop(['Ah', 'Kh', 'Qh'])
    poker.turn('Jh')
    poker.river('Th')

    odds = poker.calculate()
    assert odds[0] == 0
    assert odds[0] == 0
    assert poker.find_winner() == 2

def test_win_percentages_04():
    """
    Hustler Casino Live J4 Hand
    """

    poker = Table(8)

    # Andy
    poker.set_hole_cards(1, ['Ts', '6s'])
    poker.fold(1)

    # Mike X
    poker.set_hole_cards(2, ['Qh', '2c'])
    poker.fold(2)

    # Phil Ivey
    poker.set_hole_cards(3, ['Ah', '4d'])
    poker.fold(3)

    # Ryusuke
    poker.set_hole_cards(4, ['Kd', '2h'])
    poker.fold(4)

    # RIP
    poker.set_hole_cards(5, ['5h', '3s'])
    poker.fold(5)

    # Eric
    poker.set_hole_cards(6, ['Jd', '9s'])
    poker.fold(6)

    # Garrett
    poker.set_hole_cards(7, ['8c', '7c'])

    # Robbi
    poker.set_hole_cards(8, ['Jc', '4h'])

    odds = poker.monte_carlo(10000)
    assert odds[0:6] == [0, 0, 0, 0, 0, 0]
    assert odds[6] == pytest.approx(.5759, abs=2e-2)
    assert odds[7] == pytest.approx(.4140, abs=2e-2)

    poker.flop(['9c', 'Tc', 'Th'])
    odds = poker.calculate()
    assert odds[0:6] == [0, 0, 0, 0, 0, 0]
    assert odds[6] == pytest.approx(.6837, abs=1e-3)
    assert odds[7] == pytest.approx(.2879, abs=1e-3)

    poker.turn('3h')
    odds = poker.calculate()
    assert odds[0:6] == [0, 0, 0, 0, 0, 0]
    assert odds[6] == pytest.approx(.5312, abs=1e-3)
    assert odds[7] == pytest.approx(.4688, abs=1e-3)

    poker.river('9d')
    odds = poker.calculate()
    poker.find_winner()
    assert odds[0:6] == [0, 0, 0, 0, 0, 0]
    assert odds[6] == 0
    assert odds[7] == 1

    for player in poker.players[0:7]:
        assert player.round_won is not True

    assert poker.players[7].round_won is True
