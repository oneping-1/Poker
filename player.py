from card import Card
from typing import List

class Player:
    def __init__(self):
        self.hole: List[Card] = [None, None]
        self.folded = False

        self.__hand_score__ = 1_000_000
        self.__round_wins__ = 0
        self.__win_percentage__ = 0
        self.__seat__ = 0

    def set_hole(self, hole_cards:List[Card]):
        self.hole[0:2] = hole_cards.copy()
    
    def new_hand(self):
        self.hole = [None, None]
        self.folded = False

    def fold(self):
        self.folded = True

    def __new_combo__(self):
        self.__hand_score__ = 1_000_000

    def __new_calculation__(self):
        self.__hand_score__ = 1_000_000
        self.__round_wins__ = 0
        self.__win_percentage__ = 0
        self.__seat__ = 0