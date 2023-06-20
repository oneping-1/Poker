from player import Player
from card import Card

def test_player_01():
    player = Player(1)
    card_a = Card('A', 's', 13)
    card_b = Card('K', 'h', 14)

    player.set_hole_cards([card_a, card_b])
    assert len(player.hole_cards) == 2
    assert player.hole_cards[0].string == 'As'
    assert player.hole_cards[1].string == 'Kh'
    assert player.folded is False

    player.fold()
    assert player.folded is True
