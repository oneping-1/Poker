"""
holds Deck class which:
handles the deck
a list of the Card class with some functions
maybe add a single function to check and remove card in the future
"""

from typing import List
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

        for rank in ranks:
            for suit in suits:
                self.cards.append(Card(rank, suit))

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

    def remove_card_index(self, index:int):
        """
        removes card based off the index
        the index can be found from the check_card() function
        """
        self.cards.pop(index)
