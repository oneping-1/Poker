class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.string = f'{self.rank}{self.suit}'

    def __repr__(self):
        return self.string
