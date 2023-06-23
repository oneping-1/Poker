"""
holds Deck class which:
handles the deck
a list of the Card class with some functions
maybe add a single function to check and remove card in the future
"""

from typing import List
import random
from card import Card

class Deck:
    """
    handles the deck
    a list of the Card class with some functions
    maybe add a function to check and remove card in the future
    """
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['s', 'd', 'c', 'h']

        self.cards: List[Card] = []
        self.dead_cards: List[Card] = []

        i = 0
        for rank in ranks:
            for suit in suits:
                self.cards.append(Card(rank=rank, suit=suit, index=i))
                i += 1

    def check_card(self, card_str:str):
        """
        checks if a card (type string) is in the deck. 
        Returns index so it can be removed (popped)
        Returns none if card not found
        probably slow, maybe try a faster method in future
        """

        for index, card in enumerate(self.cards):
            if card.string == card_str:
                return index

        # maybe instead of returning None
        # return an error and then check for the error

        return None

    def remove_card_from_deck(self, *, card_str:str = None, card_index:int = None, card_random:bool = None):
        """
        removes a card from the deck from the card string or randomly
        """
        card = None

        if card_str is not None:
            for index, cards in enumerate(self.cards):
                if cards.string == card_str:
                    card = cards
                    card_index = index
                    self.cards.pop(index)
                    self.dead_cards.append(card)
                    return card
            raise ValueError(f'card {card_str} not found in deck')

        if card_index is not None:
            card = self.cards[card_index]
            self.cards.pop(card_index)
            self.dead_cards.append(card)
            return card

        if card_random is True:
            index = random.randrange(0, len(self.cards))
            card = self.cards[index]
            self.cards.pop(index)
            self.dead_cards.append(card)
            return card

    def burn(self, *,card_str:str = None, card_index:int = None, card_random:bool = None):
        """
        same as remove_card_from_deck except shorter function name
        to save space
        """
        if card_str is not None:
            self.remove_card_from_deck(card_str=card_str)

        elif card_index is not None:
            self.remove_card_from_deck(card_index=card_index)

        elif card_random is True:
            self.remove_card_from_deck(card_random=True)

        else:
            raise ValueError('no correct function inputs given')
