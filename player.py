from card import Card
from typing import List

class Player:
    def __init__(self):
        self.hole: List[Card] = [None, None]
        self.folded = False

        self.hand_score = 1_000_000
        self.round_wins = 0
        self.win_percentage = 0
        self.seat = 0

    def set_hole(self, hole_cards:List[Card]):
        self.hole[0:2] = hole_cards.copy()
    
    def new_hand(self):
        self.hole = [None, None]
        self.folded = False

    def fold(self):
        self.folded = True

    def new_combo(self):
        self.hand_score = 1_000_000

    def new_calculation(self):
        self.hand_score = 1_000_000
        self.round_wins = 0
        self.win_percentage = 0
        self.seat = 0