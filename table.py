from typing import List
import treys
from card import Card
from deck import Deck
from player2 import Player
import itertools
from tqdm import tqdm
from colorama import Fore, just_fix_windows_console
import random

just_fix_windows_console

class Table:
    def __init__(self, num_players):
        self.players: List[Player] = []

        i = 0
        while i < num_players:
            self.players.append(Player(i))
            i += 1

        self.deck = Deck()
        self.community: List[Card] = [None, None, None, None, None]

    def new_hand(self):
        for player in self.players:
            player.new_hand()
        
        self.deck = Deck()

    def set_hole_cards(self, seat_num:int, hole_cards:List[str]):
        """
        checks if both cards exist before giving them to a player
        """

        assert isinstance(seat_num, int)
        assert isinstance(hole_cards, list)
        assert len(hole_cards) == 2

        # if for some reason, someone inputs 10s or something instead of Ts
        # this should check it and fix it
        if '10' in hole_cards[0]:
            hole_cards[0] = f'T{hole_cards[0][-1]}'
        if '10' in hole_cards[1]:
            hole_cards[1] = f'T{hole_cards[1][-1]}'

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

        self.players[seat_num-1].set_hole(hole_cards)
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
                self.deck.remove_card(card)
            else:
                raise ValueError(f'Card {card} not found in deck')

        self.community[0:3] = flop_cards.copy()

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

    def calculate(self):
        """
        calculates winning percentage for each player
        """
        evaluator = treys.Evaluator()

        for player in self.players:
            player.new_calculation()

        rounds = 0

        possible_combinations = self.create_itterative_deck()

        for combo in tqdm(possible_combinations):

            for player in self.players:
                player.new_combo()
                if not player.folded:
                    player.hand_score = evaluator.evaluate(player.hole_treys, combo)

            winner_index = self.find_winner()

            if winner_index is not None:
                self.players[winner_index].round_wins += 1

            rounds += 1

        for index, player in enumerate(self.players):
            player.seat = index + 1
            player.win_percentage = player.round_wins / rounds

    def create_itterative_deck(self) -> List[List[treys.Card]]:
        permanent: List[treys.Card] = [treys.Card.new(card.string) for card in self.community if card is not None]

        combos = itertools.combinations(self.deck.cards, 5 - len(permanent))
        possible_combinations = []

        for combo in combos:
            temp_list = []
            for card in combo:
                temp_list.append(treys.Card.new(card.string))
                
            possible_combinations.append(permanent + temp_list)

        return possible_combinations
    
    def find_winner(self) -> int:
        scores = [player.hand_score for player in self.players]

        sorted_scores = sorted(scores)

        if sorted_scores[0] == sorted_scores[1]:
            return None
        else:
            return scores.index(sorted_scores[0])
        
    def fold(self, seat_num):
        self.players[seat_num-1].fold()

    def print_cards_color(self, colors:int):
        assert colors == 2 or colors == 4

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

    def random_hole_cards(self, seat_num:int):
        for i in range(0,2):
            index = random.randrange(0, len(self.deck.cards))
            self.players[seat_num-1].hole[i] = self.deck.cards[index]
            self.deck.remove_card_index(index)
        self.players[seat_num-1].treys()

    def random_flop(self):
        for i in range(0,3):
            index = random.randrange(0, len(self.deck.cards))
            self.community[i] = self.deck.cards[index]
            self.deck.remove_card_index(index)

    def random_turn(self):
        index = random.randrange(0, len(self.deck.cards))
        self.community[3] = self.deck.cards[index]
        self.deck.remove_card_index(index)

    def random_river(self):
        index = random.randrange(0, len(self.deck.cards))
        self.community[4] = self.deck.cards[index]
        self.deck.remove_card_index(index)

def main():
    game = Table(4)

    # preflop
    game.random_hole_cards(1)
    game.random_hole_cards(2)
    game.random_hole_cards(3)
    game.random_hole_cards(4)
    game.calculate()

    print()
    game.print_cards_color(4)
    print()
    for r in game.players:
        print(f'{r.seat}: {r.print_cards_color(4)} {r.win_percentage*100:6.1f}')

    # flop
    game.random_flop()
    game.calculate()

    print()
    game.print_cards_color(4)
    print()
    for r in game.players:
        print(f'{r.seat}: {r.print_cards_color(4)} {r.win_percentage*100:6.1f}')

    # turn
    game.random_turn()
    game.calculate()

    print()
    game.print_cards_color(4)
    print()
    for r in game.players:
        print(f'{r.seat}: {r.print_cards_color(4)} {r.win_percentage*100:6.1f}')

    # river
    game.random_river()
    game.calculate()
    print()
    game.print_cards_color(4)
    print()
    for r in game.players:
        print(f'{r.seat}: {r.print_cards_color(4)} {r.win_percentage*100:6.1f}')

if __name__ == '__main__':
    main()