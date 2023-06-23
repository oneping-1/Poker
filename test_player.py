from player import Player
from card import Card

def test_player_01():
    """
    tests hole cards and folds
    """
    player = Player(1)
    card_a = Card('A', 's', index=13)
    card_b = Card('K', 'h', index=14)

    player.set_hole_cards([card_a, card_b])
    assert len(player.hole_cards) == 2
    assert player.hole_cards[0].string == 'As'
    assert player.hole_cards[1].string == 'Kh'
    assert player.folded is False

    player.fold()
    assert player.folded is True

def test_player_02():
    """
    tests the players name
    """
    player = Player(1)
    player.set_name('John Doe')
    assert player.name == 'John Doe'

def test_player_03():
    """
    tests the player.calculate_outs_strings() function
    """

    player = Player(1)
    player.outs = [Card(rank='J', suit='d', index=0), Card(rank='Q', suit='c', index=1)]
    player.calculate_outs_strings()

    assert len(player.outs_string) == 2

    correct = ['Jd', 'Qc']
    for card in correct:
        assert card in player.outs_string
