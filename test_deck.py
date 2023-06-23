from deck import Deck
import pytest

def test_deck_01():
    """
    checks len of deck
    makes sure cards are removed correctly
    """
    deck = Deck()
    assert len(deck.cards) == 52

    deck.remove_card_from_deck(card_str='3c')
    assert len(deck.cards) == 51

    for card in deck.cards:
        assert card.string != '3c'

    deck.remove_card_from_deck(card_index=0)
    assert len(deck.cards) == 50

    for card in deck.cards:
        assert card.index != 0

    deck.remove_card_from_deck(card_random=True)
    assert len(deck.cards) == 49

def test_deck_02():
    """
    checks to see if error raised correctly
    if searched card is not found
    """
    deck = Deck()
    deck.remove_card_from_deck(card_str='2c')

    with pytest.raises(ValueError):
        deck.remove_card_from_deck(card_str='2c')

def test_deck_03():
    """
    checks to see if error raised correctly
    if using index
    """
    deck = Deck()

    with pytest.raises(IndexError):
        deck.remove_card_from_deck(card_index=52)

def test_deck_04():
    """
    checks deck.burn() function
    """
    deck = Deck()

    deck.burn(card_str='3c')
    assert len(deck.cards) == 51

    deck.burn(card_index=1)
    assert len(deck.cards) == 50

    for card in deck.cards:
        assert card.string != '3c'
        assert card.string != '3s'

def test_deck_05():
    """
    checks the deck.check_card() function
    """
    deck = Deck()

    index = deck.check_card('2s')
    assert index == 0

    index = deck.check_card('Ah')
    assert index == 51

    deck.burn(card_str='Tc')
    index = deck.check_card('Tc')
    assert index is None