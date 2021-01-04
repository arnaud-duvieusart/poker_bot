import random as rd
from agents.AbstractAgent import State
from game.Card import Card, Hand
from agents.AbstractAgent import Move
import logging, verboselogs

class GameOutput:

    def __init__(self, winner, amount):
        self.winner = winner
        self.amount = amount

    def __repr__(self):
        return '{} won {}$'.format(self.winner.name, self.amount)


class Game:

    last_player = None

    # try logging.DEBUG or logging.VERBOSE
    def __init__(self, player1, player2, level=logging.VERBOSE):
        self.player1 = player1
        self.player2 = player2
        self.state = State([], [], [player1.money_left, player2.money_left])
        self.deck = Deck()

        self.player1.reset_money()
        self.player2.reset_money()

        # Setting Verbose level
        self.logger = verboselogs.VerboseLogger('verbose-demo')
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(level)

    def reset_board(self):
        # Reload the deck
        self.deck = Deck()

        #Ensure null hands at the beginning
        self.player1.hand = None
        self.player2.hand = None
        self.state = State([], [], [self.player1.money_left, self.player2.money_left])

    def play(self, roundCount=20, level=logging.INFO):
        self.logger.setLevel(level)

        for _ in range(roundCount):
            self.play_round()


    def play_round(self):
        self.reset_board()

        for _ in range(2):
            self.player1.hand = Hand([self.deck.pop_card(), self.deck.pop_card()])
            self.player2.hand = Hand([self.deck.pop_card(), self.deck.pop_card()])

        # TODO: add initial pot, made of blinds

        # Draw Flop
        for _ in range(3):
            self.state.board_cards.append(self.deck.pop_card())
        output = self.play_step()
        if output:
            return output

        # Draw Turn
        self.state.board_cards.append(self.deck.pop_card())
        output = self.play_step()
        if output:
            return output

        # Draw River
        self.state.board_cards.append(self.deck.pop_card())
        return self.play_step()


    def play_step(self):
        self.logger.verbose(self.state.board_cards)

        # While the round is not finished, alternate player's move
        while self.state.last_move is None or self.state.last_move.move_type not in [Move.FOLD, Move.CALL_ALLIN, Move.CALL]:

            # Generate next move
            last_move = self.next_player.act(self.state)
            self.logger.verbose(str(self.next_player) + " " + str(last_move))

            # Save the move and go to next player
            self.state.moves.append(last_move)
            self.last_player = self.next_player

        return self.output

    @property
    def next_player(self):
        return self.player2 if self.last_player == self.player1 else self.player1


    @property
    def output(self):
        # Last player folded
        if self.state.last_move.move_type == Move.FOLD:
            self.next_player.money_left += self.state.total_pot
            return GameOutput(self.next_player, self.state.total_pot)

        # Game ended
        elif len(self.state.board_cards) == 5 and self.state.last_move.is_call:

            # Get winner
            player1_won = self.player1.hand.is_better_than(self.player2.hand, self.state.board_cards)
            winner = self.player1 if player1_won else self.player2

            winner.money_left += self.state.total_pot
            return GameOutput(winner, self.state.total_pot)


class Deck:

    def __init__(self, nbr_color=4, nbr_number=5):
        self.nbr_color = nbr_color
        self.nbr_number = nbr_number
        self.create_deck()

    def create_deck(self):
        self.deck = []
        for n in range(self.nbr_number):
            for c in range(self.nbr_color):
                card = Card(c, n)
                self.deck.append(card)

        self.shuffle()

    def shuffle(self):
        rd.shuffle(self.deck)

    def pop_card(self):
        return self.deck.pop()
