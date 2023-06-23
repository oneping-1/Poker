"""
holds Card class which:
represents each card
mainly rank and suit
"""

class Card:
    """
    represents each card
    mainly rank and suit
    """
    def __init__(self, rank, suit, *, index = None):
        self.rank:str = rank
        self.suit:str = suit
        self.index:int = index
        self.string:str = f'{self.rank}{self.suit}'

    def __repr__(self):
        return self.string
