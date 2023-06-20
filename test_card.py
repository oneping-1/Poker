from card import Card

def test_card_01():
    card = Card('2', 's', 0)

    assert card.rank == '2'
    assert card.suit == 's'
    assert card.index == 0
    assert card.string == '2s'

def test_card_02():
    card = Card('A', 'h', 51)

    assert card.rank == 'A'
    assert card.suit == 'h'
    assert card.index == 51
    assert card.string == 'Ah'
