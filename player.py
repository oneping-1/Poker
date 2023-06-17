from card import Card
from typing import List
from colorama import Fore, just_fix_windows_console
import treys
from treys import Card

just_fix_windows_console

class Player:
    def __init__(self, seat_num:int):
        self.hole: List[Card] = [None, None]
        self.hole_treys: List[treys.Card] = []
        self.folded = False
        self.seat = seat_num
        self.final_hand_name = None
        self.final_hand_score = None

        self.hand_score = 1_000_000
        self.round_wins = 0
        self.win_percentage = 0

    def set_hole(self, hole_cards:List[Card]):
        self.hole[0:2] = hole_cards.copy()
    
    def new_hand(self):
        self.hole = [None, None]
        self.hole_treys = []
        self.folded = False
        self.final_hand_name = None
        self.final_hand_score = None

    def fold(self):
        self.folded = True

    def new_combo(self):
        self.hand_score = 1_000_000

    def new_calculation(self):
        self.hand_score = 1_000_000
        self.round_wins = 0
        self.win_percentage = 0

    def print_cards_color(self, colors:int) -> str:
        final = ''
        assert colors == 2 or colors == 4

        hole_card_colors = [None, None]
        
        if colors == 2:
            for index, card in enumerate(self.hole):
                if card.suit == 's' or card.suit == 'c':
                    hole_card_colors[index] = Fore.WHITE
                elif card.suit == 'd' or card.suit == 'h':
                    hole_card_colors[index] = Fore.RED

        elif colors == 4:
            for index, card in enumerate(self.hole):
                if card.suit == 's':
                    hole_card_colors[index] = Fore.WHITE
                elif card.suit == 'd':
                    hole_card_colors[index] = Fore.BLUE
                elif card.suit == 'c':
                    hole_card_colors[index] = Fore.GREEN
                elif card.suit == 'h':
                    hole_card_colors[index] = Fore.RED

        for index, card in enumerate(self.hole):
            final += f'{hole_card_colors[index]}{card.string}{Fore.WHITE}'

            if (index + 1) != len(self.hole):
                final += ' '

        return final
            
    def treys(self):
        [self.hole_treys.append(treys.Card.new(card.string)) for card in self.hole]