from helpers.pickle_helper import save, get

class Card:

    SPADE = "SPADE"
    HEART = "HEART"
    DIAMOND = "DIAMOND"
    CLUB = "CLUB"

    def __init__(self, color, number):
        if color < 0 or color > 3:
            raise ValueError("Color should be between 0 and 3, found {}".format(color))

        self.color = color
        self.number = number


    def __repr__(self):
        color_names = [Card.SPADE, Card.HEART, Card.DIAMOND, Card.CLUB]
        return '{} of {}'.format(self.number, color_names[self.color])

    def __eq__(self, other):
        return self.color == other.color and self.number == other.number

    def __lt__(self, other):
        return self.number < other.number

    def __le__(self, other):
        return self.number <= other.number

    def __gt__(self, other):
        return self.number > other.number

    def __ge__(self, other):
        return self.number >= other.number

    def __hash__(self):
        return hash(self.__repr__())

from helpers.CombinationSimulator import FullHand

class Hand:

    def __init__(self, cards):
        if len(cards) != 2:
            raise ValueError("Hand size should be 2, but found {}".format(len(cards)))
        self._cards = cards

    # Making cards read-only to avoir errors
    @property
    def cards(self):
        return self._cards


    def __repr__(self):
        if len(self.cards) != 2:
            raise ValueError("Hand size should be 2, but found {}".format(len(self.cards)))
        return '|{} & {}|'.format(self.cards[0], self.cards[1])

    def is_better_than(self, other_hand, board_cards):
        self_fullhand = FullHand(self.cards, board_cards)
        other_fullhand = FullHand(other_hand.cards, board_cards)
        return self_fullhand.is_better_than(other_fullhand)

    def position(self, board_cards):
        fullhand = FullHand(self.cards, board_cards)
        filename = "position_cache"

        # Checking in cache
        cache = get(filename) or {}
        if cache.get(fullhand):
            return cache[fullhand]

        # Compute and save position
        else:
            res = fullhand.simulate()
            cache[fullhand] = res
            save(cache, filename)
            return res
