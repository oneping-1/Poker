from typing import List
import sys
import treys
from card import Card
from deck import Deck
from player import Player
import itertools
from tqdm import tqdm

class Table:
    def __init__(self, num_players):
        self.players: List[Player] = []

        i = 0
        while i < num_players:
            self.players.append(Player())
            i += 1

        self.deck = Deck()
        self.community = [None, None, None, None, None]

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
        if card1_index:
            hole_cards[0] = self.deck.cards[card1_index]
            self.deck.remove_card_index(card1_index)
        else:
            sys.exit(f'Card {hole_cards[0]} not found in deck')
    
        card2_index = self.deck.check_card(hole_cards[1])

        if card2_index:
            hole_cards[1] = self.deck.cards[card2_index]
            self.deck.remove_card_index(card2_index)
        else:
            sys.exit(f'Card {hole_cards[1]} not found in deck')

        self.players[seat_num-1].set_hole(hole_cards)

    def flop(self, cards:List[str]):
        """
        checks flop cards, places them on table
        """
        assert isinstance(cards, list)
        assert len(cards) == 3
        
        flop_cards = []
        for card in cards:
            index = self.deck.check_card(card)

            if index:
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
        
        if index:
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

        if index:
            self.community[4] = self.deck.cards[index]
            self.deck.remove_card_index(index)
        else:
            raise ValueError(f'card {card} not found in deck')

    def calculate(self) -> dict:
        """
        calculates winning percentage for each player
        """
        evaluator = treys.Evaluator()

        for player in self.players:
            player.__new_calculation__()

        rounds = 0

        possible_combinations = self.create_itterative_deck()

        for combo in tqdm(possible_combinations):

            for player in self.players:
                player.__new_combo__
                if not player.folded:
                    player.__hand_score__ = self.get_player_hand_score(evaluator, player.hole, combo)

            winner_index = self.find_winner()

            if winner_index is not None:
                self.players[winner_index].__round_wins__ += 1

            rounds += 1

        for index, player in enumerate(self.players):
            player.__seat__ = index + 1
            player.__win_percentage__ = player.__round_wins__ / rounds

    def create_itterative_deck(self) -> List[List[Card]]:
        permanent = [card for card in self.community if card is not None]

        combos = itertools.combinations(self.deck.cards, 5 - len(permanent))

        possible_combinations = [permanent + list(combo) for combo in combos]

        return possible_combinations
    
    def get_player_hand_score(self, evaluator:treys.Evaluator(), player_cards:List[Card], community_cards:List[Card]) -> int:

        player = [treys.Card.new(card.string) for card in player_cards]
        community = [treys.Card.new(card.string) for card in community_cards]

        return evaluator.evaluate(player, community)
    
    def find_winner(self) -> int:
        scores = [player.__hand_score__ for player in self.players]

        sorted_scores = sorted(scores)

        if sorted_scores[0] == sorted_scores[1]:
            return None
        else:
            return scores.index(sorted_scores[0])
        
    def fold(self, seat_num):
        self.players[seat_num-1].fold()

def main():
    game = Table(4)
    game.set_hole_cards(1, ['As', 'Kd'])
    game.set_hole_cards(2, ['7s', '2d'])
    game.set_hole_cards(3, ['Qd', 'Qs'])
    game.set_hole_cards(4, ['6c', '6h'])
    game.calculate()

    for r in game.players:
        print(f'{r.__seat__}: {r.__win_percentage__*100:5.2f}')

    game.flop(['9c', 'Qh', '5s'])
    game.fold(2)
    game.calculate()

    for r in game.players:
        print(f'{r.__seat__}: {r.__win_percentage__*100:5.2f}')

    game.turn('Jh')
    game.fold(4)
    game.calculate()

    for r in game.players:
        print(f'{r.__seat__}: {r.__win_percentage__*100:5.2f}')

    game.river('3c')
    game.calculate()

    for r in game.players:
        print(f'{r.__seat__}: {r.__win_percentage__*100:6.2f}')

if __name__ == '__main__':
    main()