"""
main file where everything comes together
biggest part is that it calculates odds of winning the hand
want to calculate each players outs cards in the future
"""

from typing import List
import itertools
import random
import copy
import treys
from colorama import Fore, just_fix_windows_console
#from tqdm import tqdm
from card import Card
from deck import Deck
from player import Player

just_fix_windows_console()

# need to figure out what to do in a tie after river

class Table:
    """
    method represents everything that is going on
    deck, players, community cards
    """
    def __init__(self, num_players):
        self.players: List[Player] = []

        i = 0
        while i < num_players:
            self.players.append(Player(i))
            i += 1

        for index, player in enumerate(self.players):
            player.seat = index + 1

        self.deck = Deck()
        self.community: List[Card] = [None, None, None, None, None]
        self._community_treys: List[treys.Card] = []
        self._num_winners = 0

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

    def set_hole_cards(self, seat_num:int, hole_cards:List[str]):
        """
        checks if both cards exist before giving them to a player
        """

        assert isinstance(seat_num, int)
        assert isinstance(hole_cards, list)
        assert len(hole_cards) == 2

        card1_index = self.deck.check_card(hole_cards[0])

        # need to run this first before checking for card2
        # index might change if you remove a card after checking
        if card1_index is not None:
            hole_cards[0] = self.deck.cards[card1_index]
            self.deck.remove_card_index(card1_index)
        else:
            raise ValueError(f'Card {hole_cards[0]} not found in deck')

        card2_index = self.deck.check_card(hole_cards[1])

        if card2_index is not None:
            hole_cards[1] = self.deck.cards[card2_index]
            self.deck.remove_card_index(card2_index)
        else:
            raise ValueError(f'Card {hole_cards[1]} not found in deck')
        

        self.players[seat_num-1].folded = False
        self.players[seat_num-1].hole = hole_cards.copy()
        self.players[seat_num-1].treys()

    def random_hole_cards(self, seat_num:int):
        """
        gives a given player random hole cards
        """
        for i in range(0,2):
            index = random.randrange(0, len(self.deck.cards))
            self.players[seat_num-1].hole[i] = self.deck.cards[index]
            self.deck.remove_card_index(index)
        self.players[seat_num-1].treys()

    def flop(self, cards:List[str]):
        """
        checks flop cards, places them on table
        """
        assert isinstance(cards, list)
        assert len(cards) == 3

        flop_cards = []
        for card in cards:
            index = self.deck.check_card(card)

            if index is not None:
                flop_cards.append(self.deck.cards[index])
                self.deck.remove_card_index(index)
            else:
                raise ValueError(f'Card {card} not found in deck')

        self.community[0:3] = flop_cards.copy()

    def random_flop(self):
        """
        creates a flop with random cards
        """
        for i in range(0,3):
            index = random.randrange(0, len(self.deck.cards))
            self.community[i] = self.deck.cards[index]
            self.deck.remove_card_index(index)


    def turn(self, card:str):
        """
        checks turn card, places on table
        """

        assert isinstance(card, str)

        index = self.deck.check_card(card)

        if index is not None:
            self.community[3] = self.deck.cards[index]
            self.deck.remove_card_index(index)
        else:
            raise ValueError(f'card {card} not found in deck')

    def random_turn(self):
        """
        creates a turn with a random card
        """
        index = random.randrange(0, len(self.deck.cards))
        self.community[3] = self.deck.cards[index]
        self.deck.remove_card_index(index)

    def river(self, card:str):
        """
        check river cards, places on table
        """

        assert isinstance(card, str)

        index = self.deck.check_card(card)

        if index is not None:
            self.community[4] = self.deck.cards[index]
            self.deck.remove_card_index(index)
        else:
            raise ValueError(f'card {card} not found in deck')

    def random_river(self):
        """
        creates a river with a random card
        """
        index = random.randrange(0, len(self.deck.cards))
        self.community[4] = self.deck.cards[index]
        self.deck.remove_card_index(index)

    def calculate(self) -> List[float]:
        """
        calculates winning percentage for each player
        returns a list of floats but only used for pytests
        """
        self._create_community_treys()
        evaluator = treys.Evaluator()
        win_percentages: List[float] = []

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
                    player.hand_score = evaluator.evaluate(player.hole_treys, combo)

            winner_index = self._find_lowest_score()

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

    def _find_lowest_score(self) -> int:
        """
        finds the winner based of each players hand
        returns None if there is a tie
        returns seat index (seat num - 1) if no tie
        """
        scores = [player.hand_score for player in self.players]

        sorted_scores = sorted(scores)

        if sorted_scores[0] == sorted_scores[1]:
            return None
        else:
            return scores.index(sorted_scores[0])

    def monte_carlo(self, num_runs=1500):
        """
        used to calculate odds preflop
        due to intense computation to run through
        all combinations of possible
        community cards
        """
        evaluator = treys.Evaluator()
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
                card = temp_deck.random_card()
                temp_community_treys.append(treys.Card.new(card.string))

            for player in self.players:
                player.new_combo()
                if not player.folded:
                    player.hand_score = evaluator.evaluate(player.hole_treys, temp_community_treys)

            winner_index = self._find_lowest_score()

            if winner_index is not None:
                self.players[winner_index].round_wins += 1

        for player in self.players:
            player.win_percentage = player.round_wins / num_runs
            win_percentages.append(player.win_percentage)

        return win_percentages

    def find_winner(self) -> int:
        """
        finds the winner of the hand
        after river card
        returns number of winners for testing purposes
        """
        assert len(self.community) == 5
        self._create_community_treys()
        assert len(self._community_treys) == 5

        evaluator = treys.Evaluator()

        best_hand = 1_000_000
        self._num_winners = 0

        for player in self.players:
            if not player.folded:
                player.final_hand_score = evaluator.evaluate(player.hole_treys, self._community_treys)
                hand_rank = evaluator.get_rank_class(player.final_hand_score)
                player.final_hand_name = evaluator.class_to_string(hand_rank)

            if player.final_hand_score < best_hand:
                best_hand = player.final_hand_score

        for player in self.players:
            if best_hand == player.final_hand_score:
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
                    hand_name = player.final_hand_name

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
    game.monte_carlo()
    game.print_table(4)

    # flop
    game.random_flop()
    game.calculate()
    game.print_table(4)

    # turn
    game.random_turn()
    game.calculate()
    game.print_table(4)

    # river
    game.random_river()
    game.find_winner()
    game.print_table(4)

if __name__ == '__main__':
    main()
