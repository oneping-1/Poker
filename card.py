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
    def __init__(self, rank, suit, index):
        self.rank = rank
        self.suit = suit
        self.index = index
        self.string = f'{self.rank}{self.suit}'

    def __repr__(self):
        return self.string
