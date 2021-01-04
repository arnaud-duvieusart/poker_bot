import random as rd


class AbstractAgent:

    hand = None

    def __init__(self, name, initial_money):
        self.name = name

        if initial_money <= 0:
            raise ValueError("The amount of money left has to be a positive number.")
        self.initial_money = initial_money
        self.money_left = initial_money

    def __repr__(self):
        return '{}'.format(self.name)

    def reset_money(self):
        self.money_left = self.initial_money

    def act(self, state):
        if state.last_move is not None:
            if state.last_move.move_type == Move.FOLD:
                raise Exception("Cannot act on Fold.")

    def spend(self, amount):
        # If the player has enough money, spend it and return True
        if amount <= self.money_left:
            self.money_left = self.money_left - amount
            return True

        # Otherwhise return False
        return False


class State:

    def __init__(self, board_cards, moves, stacks):
        self.___board_cards = board_cards
        self.__moves = moves
        self.__stacks = stacks

    @property
    def last_move(self):
        if len(self.moves) == 0:
            return None
        else:
            return self.moves[-1]

    def __eq__(self, other_state):
        #check neq

        # Quick checks
        if not isinstance(other_state, self.__class__):
            return False
        elif len(self.moves) != len(other_state.moves):
            return False
        elif self.last_move != other_state.last_move:
             return False
        elif self.last_move.price_stats(self) != other_state.last_move.price_stats(self):
            return False
        for move, other_move in zip(self.moves, other_state.moves):
            if move != other_move:
                return False

        # Compare positions
        if self.next_player_position != other_state.next_player_position:
            return False

        return True

    def __ne__(self, other_state):
        return not self == other_state

    @property
    def moves(self):
        return self.__moves

    @property
    def board_cards(self):
        return self.___board_cards

    @property
    def total_pot(self):
        """
        For each move we retreive the call_value and if the last move is a raise we add this raise value.
        """
        res = 0
        for (i, move) in enumerate(self.moves):

            if move.move_type == Move.CALL_ALLIN:
                res += move.call_allin_val
            #elif len(self.moves) == i + 1 and move.move_type == Move.RAISE:
            #    res = res + move.call_val + move.raise_val
            else:
                res = res + move.call_val + move.raise_val
        return res


#     @property
#     def can_check(self):
#         if len(moves) == 0:
#             return True
#         else:
#             last_move = moves[-1]
#             return last_move

from helpers.discretizer import discretize, discretize_price

class PriceValue:

    def __init__(self, relative_to_bidder, relative_to_me, relative_to_pot):
        self.__relative_to_bidder = discretize_price(relative_to_bidder)
        self.__relative_to_me = discretize_price(relative_to_me)
        self.__relative_to_pot = discretize_price(relative_to_pot)

    def __eq__(self, other_val):
        return isinstance(other_val, self.__class__) and self.relative_to_me == other_val.relative_to_me and self.relative_to_bidder == other_val.relative_to_bidder \
            and self.relative_to_pot == other_val.relative_to_pot

    def __ne__(self, other_val):
        return not self == other_val
    
    @property
    def relative_to_bidder(self):
        return self.__relative_to_bidder

    @property
    def relative_to_pot(self):
        return self.__relative_to_pot

    @property
    def relative_to_me(self):
        return self.__relative_to_me

class Move:

    CALL = "CALL"
    RAISE = "RAISE"
    FOLD = "FOLD"
    CALL_ALLIN = "CALL_ALLIN"

    def __init__(self, move_type, money_left, call_val=0, raise_val=0, call_allin_val=0):

        self.move_type = move_type

        # The call value represents the amount called, from the past round
        self.__call_val = call_val
        self.__money_left = money_left

        # The raise value is the value to be called the next round
        self.__raise_val = raise_val

        if move_type == Move.CALL_ALLIN:
            self.__call_allin_val = call_allin_val

        if self.future_call > money_left:
            raise ValueError()

    def __repr__(self):
        return 'Move type: {}, Call value: {}, Raise value: {}'.format(self.move_type, self.__call_val, self.__raise_val)

    def price_stats(self, state):
        return PriceValue(self.future_call / self.__money_left, self.future_call / state.next_player.money_left, self.future_call / state.total_pot)

    def __eq__(self, other_move):
        #check case
        if isinstance(other_move, self.__class__):
            if self.future_call == 0 and other_move.future_call == 0:
                return True
            else:
                return self.move_type == other_move.move_type and self.future_call_relative == other_move.future_call_relative \
                    and self.raised_ratio == other_move.raised_ratio
        return False

    def __ne__(self, other_move):
        return not self == other_move

    @property
    def call_val(self):
        return self.__call_val

    @property
    def raise_val(self):
        return self.__raise_val

    @property
    def call_allin_val(self):
        return self.__call_allin_val

    @property
    def future_call(self):
        if self.__call_allin_val != 0:
            return self.__call_allin_val
        else:
            return self.call_val + self.raise_val

    @property
    def raised_ratio(self):
        return discretize_price(self.raise_val / self.future_call)

    @property
    def future_call_relative(self):
        if self.future_call == 0:
            return 0
        else:
            return discretize_price(self.future_call / self.__money_left)

    @property
    def is_call(self):
        return self.move_type in [Move.CALL, Move.CALL_ALLIN]

    @staticmethod
    def Call(call_val):
        return Move(Move.CALL, call_val)

    @staticmethod
    def CallAllIn(call_val, call_allin_val):
        return Move(Move.CALL_ALLIN, call_val, call_allin_val= call_allin_val)

    @staticmethod
    def Fold():
        return Move(Move.FOLD)

    @staticmethod
    def Raise(call_val, raise_val):
        return Move(Move.RAISE, call_val, raise_val)
