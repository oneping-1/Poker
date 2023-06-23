"""
holds Player class which:
handles all player logic
hole cards, fold status, win percentage
"""

from typing import List
import treys
from colorama import Fore, just_fix_windows_console
from card import Card

just_fix_windows_console()

class Player:
    """
    handles all player logic
    hole cards, fold status, win percentage
    """
    def __init__(self, seat_num:int):
        assert isinstance(seat_num, int)
        assert seat_num > 0

        self.hole_cards: List[Card] = [None, None]
        self.hole_treys: List[treys.Card] = []
        self.folded = False
        self.seat = seat_num
        self.hand_name = None
        self.hand_score = 1_000_000
        self.outs: List[Card] = []
        self.outs_string: List[str] = []
        self.name: str = None

        # can handle ties
        self.round_won = False

        self.temp_hand_score = 1_000_000
        self.round_wins = 0
        self.win_percentage = 0

    def __repr__(self):
        hole_card_strings = [card.string for card in self.hole_cards]
        return f'seat={self.seat} | hole_cards={hole_card_strings} | fold={self.folded}'

    def set_name(self, name_str:str):
        """
        sets the players name
        """
        self.name = name_str

    def new_hand(self):
        """
        gets the player ready for a new hand
        resets hole cards, fold status, and hand score
        """
        self.hole_cards = [None, None]
        self.hole_treys = []
        self.folded = False
        self.hand_name = None
        self.hand_score = 1_000_000
        self.round_won = False
        self.outs: List[Card] = []

    def fold(self):
        """
        makes the fold status true
        """
        self.folded = True
        self.win_percentage = 0

    def set_hole_cards(self, hole_cards:List[Card]):
        """
        sets the hole cards for the player and creates treys object
        """
        assert isinstance(hole_cards, List)
        assert len(hole_cards) == 2

        for index, card in enumerate(hole_cards):
            self.hole_cards[index] = card

        self.treys()

    def new_combo(self):
        """
        resets the hand score for each combination of community cards
        """
        self.temp_hand_score = 1_000_000

    def new_calculation(self):
        """
        resets the round wins and win percentage
        for a new calculation
        """
        self.temp_hand_score = 1_000_000
        self.round_wins = 0
        self.win_percentage = 0

    def print_cards_color(self, colors:int) -> str:
        """
        prints the players hole cards in given number of colors
        1 colors = black
        2 colors = black, red
        4 colors = black, blue, green, red
        """
        final = ''
        assert colors == 1 or colors == 2 or colors == 4

        hole_card_colors = [None, None]

        if colors == 1:
            hole_card_colors = [Fore.WHITE, Fore.WHITE].copy()

        if colors == 2:
            for index, card in enumerate(self.hole_cards):
                if card.suit == 's' or card.suit == 'c':
                    hole_card_colors[index] = Fore.WHITE
                elif card.suit == 'd' or card.suit == 'h':
                    hole_card_colors[index] = Fore.RED

        elif colors == 4:
            for index, card in enumerate(self.hole_cards):
                if card.suit == 's':
                    hole_card_colors[index] = Fore.WHITE
                elif card.suit == 'd':
                    hole_card_colors[index] = Fore.BLUE
                elif card.suit == 'c':
                    hole_card_colors[index] = Fore.GREEN
                elif card.suit == 'h':
                    hole_card_colors[index] = Fore.RED

        for index, card in enumerate(self.hole_cards):
            final += f'{hole_card_colors[index]}{card.string}{Fore.WHITE}'

            if (index + 1) != len(self.hole_cards):
                final += ' '

        return final

    def calculate_outs_strings(self):
        """
        calculates the strings for out cards for unit tests
        returns list for testing
        """
        for card in self.outs:
            self.outs_string.append(card.string)

    def treys(self):
        """
        sets the players hole cards as trey cards
        this optimizes the calculations as dont need to create a
        new treys.Card instance for each combination of community cards
        """

        for card in self.hole_cards:
            self.hole_treys.append(treys.Card.new(card.string))
