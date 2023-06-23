# pylint: disable=protected-access

import pytest
from table import Table

def test_table_01():
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

def test_table_02():
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

def test_table_03():
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

def test_table_04():
    """
    Hustler Casino Live J4 Hand
    """

    poker = Table(8)

    poker.set_player_name(1, 'Andy')
    poker.set_hole_cards(1, ['Ts', '6s'])
    poker.fold(1)

    poker.set_player_name(2, 'Mike X')
    poker.set_hole_cards(2, ['Qh', '2c'])
    poker.fold(2)

    poker.set_player_name(3, 'Phil Ivey')
    poker.set_hole_cards(3, ['Ah', '4d'])
    poker.fold(3)

    poker.set_player_name(4, 'Ryusuke')
    poker.set_hole_cards(4, ['Kd', '2h'])
    poker.fold(4)

    poker.set_player_name(5, 'RIP')
    poker.set_hole_cards(5, ['5h', '3s'])
    poker.fold(5)

    poker.set_player_name(6, 'Eric')
    poker.set_hole_cards(6, ['Jd', '9s'])
    poker.fold(6)

    poker.set_player_name(7, 'Garrett')
    poker.set_hole_cards(7, ['8c', '7c'])

    poker.set_player_name(8, 'Robbi')
    poker.set_hole_cards(8, ['Jc', '4h'])

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
    assert odds[0:7] == [0, 0, 0, 0, 0, 0, 0]
    assert odds[7] == 1

    for player in poker.players[0:7]:
        assert player.round_won is not True

    assert poker.players[7].round_won is True

def test_table_05():
    """
    tests player out cards
    """
    table = Table(2)

    table.set_hole_cards(1, ['Ac', 'Qh'])
    table.set_hole_cards(2, ['Ah', 'Kh'])
    assert len(table.deck.cards) == 48

    table.flop(['8c', '3s', 'Th'])
    table.river('9d')
    assert len(table.deck.cards) == 44

    odds = table.calculate()
    table.find_outs()

    assert odds[0] == pytest.approx(0.1591, abs=1e-3)
    assert odds[1] == pytest.approx(0.8409, abs=1e-3)

    assert len(table.players[0].outs) == 7

    correct_outs = ['Js', 'Qs', 'Jd', 'Qd', 'Jh', 'Jc', 'Jc']
    for correct in correct_outs:
        assert correct in table.players[0].outs_string

def test_table_06():
    """
    Hustler Casion Live Full House vs Flush
    https://www.youtube.com/watch?v=7YmZeQaX4r0
    """

    table = Table(6)

    table.set_player_name(1, 'Ben')
    table.set_hole_cards(1, ['Ad', 'Jd'])

    table.set_player_name(2, 'JRB')
    table.set_hole_cards(2, ['Kh', '4h'])

    table.set_player_name(3, 'Aussie Matt')
    table.set_hole_cards(3, ['Ac', '8c'])

    table.set_player_name(4, 'Huss')
    table.set_hole_cards(4, ['Qc', '2c'])
    table.fold(4)

    table.set_player_name(5, 'Tony G')
    table.set_hole_cards(5, ['Ah', '3s'])
    table.fold(5)

    table.set_player_name(6, 'Charles')
    table.set_hole_cards(6, ['Td', '5c'])
    table.fold(6)

    table.flop(['6d', '4s', '4d'])
    table.calculate()

    assert table.players[0].win_percentage == pytest.approx(0.2538, abs=1e-3)
    assert table.players[1].win_percentage == pytest.approx(0.7282, abs=1e-3)
    assert table.players[2].win_percentage == pytest.approx(0.0135, abs=1e-3)

    table.fold(3)
    table.calculate()

    assert table.players[0].win_percentage == pytest.approx(0.2538, abs=1e-3)
    assert table.players[1].win_percentage == pytest.approx(0.7417, abs=1e-3)

    table.turn('Kd')
    table.calculate()

    assert table.players[0].win_percentage == 0
    assert table.players[1].win_percentage == 1

    table.find_outs()

    assert len(table.players[1].outs) == len(table.deck.cards)
    assert len(table.players[0].outs) == 0

    table.river('2s')
    table.calculate()
    table.find_winner()

    assert table.players[0].win_percentage == 0
    assert table.players[1].win_percentage == 1

    assert table.players[0].hand_name == 'Flush'
    assert table.players[1].hand_name == 'Full House'

def test_table_07():
    """
    check table._create_iterative_deck()
    """

    table = Table(2)

    table.set_hole_cards(1, ['8c', '2h'])
    table.set_hole_cards(2, ['Ac', 'Kd'])

    table.flop(['2c', 'Td', 'As'])

    iterative_deck = table._create_iterative_deck()
    assert len(iterative_deck) == 990

def test_table_08():
    """
    tests table._find_lowest_score()
    """

    table = Table(1)

    hand_scores = [1000, 100, 500, 400, 320, 10402]
    index = table._find_lowest_score(hand_scores)
    assert index == 1

    hand_scores = [1000, 10000]
    index = table._find_lowest_score(hand_scores)
    assert index == 0

    hand_scores = [30, 4320, 16000, 420, 3, 19, 204, 730, 5000]
    index = table._find_lowest_score(hand_scores)
    assert index == 4

def test_table_09():
    """
    tests table._find_lowest_score() for ties
    """

    table = Table(1)

    hand_scores = [4, 16, 2000, 2000, 4]
    index = table._find_lowest_score(hand_scores)
    assert index is None

    hand_scores = [420, 420]
    index = table._find_lowest_score(hand_scores)
    assert index is None

    hand_scores = [52, 420, 69, 165, 1600, 5000, 52, 69, 52]
    index = table._find_lowest_score(hand_scores)
    assert index is None
