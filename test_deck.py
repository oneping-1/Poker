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
