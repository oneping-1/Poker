from card import Card
from typing import List

class Deck:
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
    
    def remove_card(self, card:str):
        index = self.check_card(card)

        if index is not None:
            self.cards.pop(index)
        else:
            raise ValueError('index out of range')

    def remove_card_index(self, index:int):
        try:
            self.cards.pop(index)
        except IndexError:
            raise ValueError('index out of range')
