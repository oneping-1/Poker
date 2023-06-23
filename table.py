"""
main file where everything comes together
biggest part is that it calculates odds of winning the hand
want to calculate each players outs cards in the future
"""

from typing import List
import itertools
import copy
import treys
from colorama import Fore, just_fix_windows_console
#from tqdm import tqdm
from card import Card
from deck import Deck
from player import Player

just_fix_windows_console()

class Table:
    """
    method represents everything that is going on
    deck, players, community cards
    """
    def __init__(self, num_players:int):
        assert isinstance(num_players, int)
        assert num_players > 0

        self.players: List[Player] = []

        i = 1
        while i <= num_players:
            self.players.append(Player(i))
            i += 1

        for index, player in enumerate(self.players):
            player.seat = index + 1

        self.deck = Deck()
        self.community: List[Card] = [None, None, None, None, None]
        self._community_treys: List[treys.Card] = []
        self._num_winners: int = 0
        self._evaluator: treys.Evaluator = treys.Evaluator()

    def _create_community_treys(self):
        self._community_treys: List[treys.Card] = []
        for card in self.community:
            if card is not None:
                self._community_treys.append(treys.Card.new(card.string))

    def new_hand(self):
        """
        function is used after each hand is completed
        resets deck and each players hole cards
        """
        for player in self.players:
            player.new_hand()

        self.deck = Deck()
        self._num_winners = 0

    def fold(self, seat_num):
        """
        folds the player for given seat number
        """
        self.players[seat_num-1].fold()

    def set_player_name(self, seat_num:int, name:str):
        """
        sets the players name from the table class
        """
        self.players[seat_num-1].set_name(name_str=name)

    def set_hole_cards(self, seat_num:int, hole_cards:List[str]):
        """
        checks if both cards exist before giving them to a player
        """
        assert isinstance(seat_num, int)
        assert isinstance(hole_cards, list)
        assert len(hole_cards) == 2

        hole_card_objects = []
        hole_card_objects.append(self.deck.remove_card_from_deck(card_str=hole_cards[0]))
        hole_card_objects.append(self.deck.remove_card_from_deck(card_str=hole_cards[1]))

        self.players[seat_num-1].folded = False
        self.players[seat_num-1].set_hole_cards(hole_card_objects)

    def random_hole_cards(self, seat_num:int):
        """
        gives a given player random hole cards
        """
        hole_cards = []
        for _ in range(0,2):
            hole_cards.append(self.deck.remove_card_from_deck(card_random=True))
        self.players[seat_num-1].set_hole_cards(hole_cards)

    def flop(self, card_strs:List[str]):
        """
        checks flop cards, places them on table
        """
        assert isinstance(card_strs, list)
        assert len(card_strs) == 3

        flop_cards = []
        for card in card_strs:
            flop_cards.append(self.deck.remove_card_from_deck(card_str=card))

        self.community[0:3] = flop_cards.copy()
        self._create_community_treys()

    def random_flop(self):
        """
        creates a flop with random cards
        """
        flop_cards = []
        for _ in range(0,3):
            flop_cards.append(self.deck.remove_card_from_deck(card_random=True))

        self.community[0:3] = flop_cards.copy()

    def turn(self, card_str:str):
        """
        checks turn card, places on table
        """
        assert isinstance(card_str, str)
        self.community[3] = self.deck.remove_card_from_deck(card_str=card_str)
        self._create_community_treys()

    def random_turn(self):
        """
        creates a turn with a random card
        """
        self.community[3] = self.deck.remove_card_from_deck(card_random=True)

    def river(self, card_str:str):
        """
        check river cards, places on table
        """
        assert isinstance(card_str, str)
        self.community[4] = self.deck.remove_card_from_deck(card_str=card_str)
        self._create_community_treys()

    def random_river(self):
        """
        creates a river with a random card
        """
        self.community[4] = self.deck.remove_card_from_deck(card_random=True)

    def calculate(self) -> List[float]:
        """
        calculates winning percentage for each player
        returns a list of floats but only used for pytests
        """
        evaluator = treys.Evaluator()
        win_percentages: List[float] = []
        self._create_community_treys()

        if len(self._community_treys) == 5:
            self.find_winner()

        for player in self.players:
            player.new_calculation()

        rounds = 0

        possible_combinations = self._create_iterative_deck()

        # spot 1 for tqdm
        for combo in (possible_combinations):

            for player in self.players:
                player.new_combo()
                if not player.folded:
                    player.temp_hand_score = evaluator.evaluate(player.hole_treys, combo)

            hand_scores = [player.temp_hand_score for player in self.players]
            winner_index = self._find_lowest_score(hand_scores)

            if winner_index is not None:
                self.players[winner_index].round_wins += 1

            rounds += 1

        for player in self.players:
            player.win_percentage = player.round_wins / rounds
            win_percentages.append(player.win_percentage)

        return win_percentages

    def _create_iterative_deck(self) -> List[List[treys.Card]]:
        """
        creates a list of all possible community card runouts
        """
        combos = itertools.combinations(self.deck.cards, 5 - len(self._community_treys))
        possible_combinations = []

        for combo in combos:
            temporary_community_cards = []
            for card in combo:
                temporary_community_cards.append(treys.Card.new(card.string))

            possible_combinations.append(self._community_treys + temporary_community_cards)

        return possible_combinations

    def _find_lowest_score(self, hand_scores: List[int]) -> int:
        """
        finds the winner based of each players hand
        returns None if there is a tie
        returns seat index (seat num - 1) if no tie
        """
        sorted_scores = sorted(hand_scores)

        if sorted_scores[0] == sorted_scores[1]:
            return None
        else:
            return hand_scores.index(sorted_scores[0])

    def monte_carlo(self, num_runs=1500):
        """
        used to calculate odds preflop
        due to intense computation to run through
        all combinations of possible
        community cards
        """
        evaluator = treys.Evaluator()
        t_e = evaluator

        win_percentages: List[float] = []

        for player in self.players:
            player.new_calculation()

        permanent_community = self.community.copy()

        permanent_community_treys = []
        for card in permanent_community:
            if card is not None:
                permanent_community_treys.append(treys.Card.new(card.string))

        # spot 2 for tqdm
        for _ in (range(0, num_runs)):
            temp_community_treys = permanent_community_treys.copy()
            temp_deck = copy.deepcopy(self.deck)
            while len(temp_community_treys) < 5:
                card = temp_deck.remove_card_from_deck(card_random=True)
                temp_community_treys.append(treys.Card.new(card.string))

            for player in self.players:
                player.new_combo()
                if not player.folded:
                    player.temp_hand_score = t_e.evaluate(player.hole_treys, temp_community_treys)

            hand_scores = [player.temp_hand_score for player in self.players]
            winner_index = self._find_lowest_score(hand_scores)

            if winner_index is not None:
                self.players[winner_index].round_wins += 1

        for player in self.players:
            player.win_percentage = player.round_wins / num_runs
            win_percentages.append(player.win_percentage)

        return win_percentages

    def find_outs(self):
        """
        finds the river card each player would need to win the hand
        """
        self._create_community_treys()
        assert len(self._community_treys) == 4

        temp_community_treys = self._community_treys.copy()
        temp_community_treys.append(None)
        assert len(temp_community_treys) == 5

        for card in self.deck.cards:
            temp_community_treys[4] = treys.Card.new(card.string)
            winner_index = self._find_outs_winner(temp_community_treys)

            if winner_index is not None:
                self.players[winner_index].outs.append(card)

        for player in self.players:
            player.calculate_outs_strings()

    def _find_outs_winner(self, community_cards: List[treys.Card]) -> int:
        lowest_score = 10_000_000

        for index, player in enumerate(self.players):
            if player.folded is False:
                player.temp_hand_score = self._evaluator.evaluate(player.hole_treys, community_cards)
                if player.temp_hand_score < lowest_score:
                    lowest_score = player.temp_hand_score
                    lowest_score_index = index
                elif player.temp_hand_score == lowest_score:
                    lowest_score_index = None

        return lowest_score_index

    def find_winner(self) -> int:
        """
        finds the winner of the hand
        after river card
        returns number of winners for testing purposes
        """
        assert len(self.community) == 5
        self._create_community_treys()
        assert len(self._community_treys) == 5

        best_hand = 1_000_000
        self._num_winners = 0

        for player in self.players:
            if not player.folded:
                player.hand_score = self._evaluator.evaluate(player.hole_treys, self._community_treys)
                hand_rank = self._evaluator.get_rank_class(player.hand_score)
                player.hand_name = self._evaluator.class_to_string(hand_rank)

            if player.hand_score < best_hand:
                best_hand = player.hand_score

        for player in self.players:
            if best_hand == player.hand_score:
                player.round_won = True
                self._num_winners += 1

        return self._num_winners

    def print_community_cards_color(self, colors:int):
        """
        prints everything on the table
        community cards, each players hole cards and win percentage
        """
        assert colors in (2, 4)

        community_card_colors = [None, None, None, None, None]

        if colors == 2:
            for index, card in enumerate(self.community):
                if card is not None:
                    if card.suit == 's' or card.suit == 'c':
                        community_card_colors[index] = Fore.WHITE
                    elif card.suit == 'd' or card.suit == 'h':
                        community_card_colors[index] = Fore.RED

        elif colors == 4:
            for index, card in enumerate(self.community):
                if card is not None:
                    if card.suit == 's':
                        community_card_colors[index] = Fore.WHITE
                    elif card.suit == 'd':
                        community_card_colors[index] = Fore.BLUE
                    elif card.suit == 'c':
                        community_card_colors[index] = Fore.GREEN
                    elif card.suit == 'h':
                        community_card_colors[index] = Fore.RED

        for index, card in enumerate(self.community):
            if card is not None:
                print(f'{community_card_colors[index]}{card.string}{Fore.WHITE}', end=' ')

            if (index+1) == len(self.community):
                print()

    def print_table(self, num_colors=2):
        """
        prints community cards and player hole cards
        also prints each players odds of winning hand
        """

        print()
        self.print_community_cards_color(num_colors)

        if len(self._community_treys) == 5:
            self.find_winner()
            for player in self.players:
                if not player.folded:
                    seat = player.seat
                    hole_cards = player.print_cards_color(num_colors)
                    hand_name = player.hand_name

                    if player.round_won:
                        if self._num_winners == 1:
                            round_won = '#'
                        else:
                            round_won = '+'
                    else:
                        round_won = ' '

                    print(f'{seat:2d}: {hole_cards} {round_won} {hand_name}')
        else:
            for player in self.players:
                if not player.folded:
                    seat = player.seat
                    hole_cards = player.print_cards_color(num_colors)
                    win_percentage = player.win_percentage

                    print(f'{seat:2d}: {hole_cards} {win_percentage*100:6.1f}')

def main():
    """
    main function to check for obvious errors
    and check math with online calculators
    """
    game = Table(9)

    # pre-flop
    game.random_hole_cards(1)
    game.random_hole_cards(2)
    game.random_hole_cards(3)
    game.random_hole_cards(4)
    game.random_hole_cards(5)
    game.random_hole_cards(6)
    game.random_hole_cards(7)
    game.random_hole_cards(8)
    game.random_hole_cards(9)

    # flop
    game.random_flop()
    game.calculate()
    game.print_table(4)

    # turn
    game.random_turn()
    game.calculate()
    game.print_table(4)
    game.find_outs()

    # river
    game.random_river()
    game.find_winner()
    game.print_table(4)

if __name__ == '__main__':
    main()
