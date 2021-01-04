from collections import defaultdict
import itertools as t
from collections import Counter
import operator
import random
from random import shuffle
from game.Card import Card
import time

class FullHand: #A hand is a list of visible cards. Not necessarly a "hand" as it can be composed of the board

    def __init__(self, hand, board_cards):
        # Hand cards
        self.cards = hand + board_cards

    def __repr__(self):
        return '|{}|'.format(self.cards)

    def __hash__(self):
        return hash(tuple(self.cards))

    def __eq__(self, other_hand):
        if len(self.cards) != len(other_hand.cards):
            return False
        for (card_a, card_b) in zip(self.cards, other_hand.cards):
            if card_a != card_b:
                return False
        return True

    def is_better_than(self, other_hand):
        '''Check if self is a better hand than other_hand. Warning, draws are possible'''
        my_hand, my_cards = self.check_hand_smart()
        adversary_hand, adversary_cards = other_hand.check_hand_smart()
        if (my_hand > adversary_hand):
            return True
        elif my_hand == adversary_hand and (my_hand == 7 or my_hand == 3): #Full house or double pairs
            if my_cards[0] > adversary_cards[0]:
                return True
            elif my_cards[0] == adversary_cards[0] and my_cards[1] > adversary_cards[1]:
                return True
        return False

    def is_draw(self, other_hand):
        '''Check if self and other_hand would draw'''
        my_hand, my_cards = self.check_hand_smart()
        adversary_hand, adversary_cards = other_hand.check_hand_smart()
        return my_hand == adversary_hand and my_cards == adversary_cards

    def check_hand_smart(self, my_hand = 1):
        '''returns a tuple (score, cards)
        score : int corresponding to the score of the hand
        cards : cards composing this hand for potential comparisons

        arg my_hand : if method is used to compare 2 hands, my_hand is the comparison score so that we may not have to go all the way
        '''
        one_pair, one_pair_cards = self.check_one_pair()
        straight, straight_cards = self.check_straight(True)
        flush, flush_cards = self.check_flush()
        if flush and straight:
            if len(set(flush_cards).intersection(set(straight_cards)))>=5:
                cards = set(flush_cards).intersection(set(straight_cards))
                return 9, sorted(list(cards), key = lambda x : x.number)[-1].number
        if my_hand == 9:
            return -1,-1
        if one_pair:
            two_pairs, two_pairs_cards = self.check_two_pairs()
            three_of_a_kind, three_of_a_kind_cards = self.check_three_of_a_kind()
            #Not SF
            if three_of_a_kind:
                four_of_a_kind, four_of_a_kind_cards = self.check_four_of_a_kind()
                if four_of_a_kind:
                    return 8, four_of_a_kind_cards
                if my_hand == 8:
                    return -1,-1
                if two_pairs:
                    pair = None
                    for i in two_pairs_cards:
                        if i != three_of_a_kind_cards:
                            pair = i
                    return 7, (three_of_a_kind_cards, pair)#FULL HOUSE
                if flush:
                    return 6, flush_cards
                if straight:
                    return 5, straight_cards
                return 4, three_of_a_kind_cards
            if two_pairs:
                return 3, two_pairs_cards
            return 2, one_pair_cards
        else: #No pair
            if flush:
                return 6, flush_cards
            if straight:
                return 5, straight_cards
            return 1, max(x.number for x in self.cards)


    def check_hand(self, my_hand = 1):
        '''USE check_hand_smart instead'''
        straight_flush, cards = self.check_straight_flush()
        if straight_flush:
            return 9, cards
        if my_hand == 9:
            return -1,-1
        four_of_a_kind, cards = self.check_four_of_a_kind()
        if four_of_a_kind:
            return 8, cards
        if my_hand == 8:
            return -1,-1
        full_house, cards = self.check_full_house()
        if full_house:
            return 7, cards
        if my_hand == 7:
            return -1,-1
        flush, cards = self.check_flush()
        if flush:
            return 6, cards
        if my_hand == 6:
            return -1,-1
        straight, cards = self.check_straight()
        if straight:
            return 5, cards
        if my_hand == 5:
            return -1,-1
        three_of_a_kind, cards = self.check_three_of_a_kind()
        if three_of_a_kind:
            return 4, cards
        if my_hand == 4:
            return -1,-1
        two_pairs, cards = self.check_two_pairs()
        if two_pairs:
            return 3, cards
        if my_hand == 3:
            return -1,-1
        one_pair, cards = self.check_one_pair()
        if one_pair:
            return 2, cards
        if my_hand == 2:
            return -1,-1
        return 1, max(x.numbers for x in self.cards) #ADD HIGH CARD

    def check_straight_flush(self):
        present_straight, cards_of_straight = check_straight(self, straight_flush = True)
        present_flush, cards_of_flush = check_flush(self)
        if present_straight and present_flush:
            cards = set(cards_of_flush).intersection(set(cards_of_straight))
            if len(cards)>=5:
                return True, list(cards).sort(key = lambda x : x[0])[-1][0]
            else:
                return False, -1
        else:
            return False, -1

    def check_four_of_a_kind(self):
        values = [i.number for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        if sorted(value_counts.values())[-1] >= 4:
            return True, max(Counter(value_counts).items(), key=operator.itemgetter(1))[0]
        return False, -1

    def check_full_house(self):
        values = [i.number for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        appearances = sorted(value_counts.values())
        if appearances[-1]>= 3 and appearances[-2]>=2:
            triple_candidates = {k: v for k, v in value_counts.items() if v >=3}
            max_triple = max(Counter(triple_candidates).items(), key=operator.itemgetter(0))[0]
            double_candidates = {k: v for k, v in value_counts.items() if v >=2 and k != max_triple}
            max_double = max(Counter(double_candidates).items(), key=operator.itemgetter(0))[0]
            return True, (max_triple, max_double)
        return False, -1

    def check_flush(self):
        suits = [i.color for i in self.cards]
        if max(Counter(suits).values())>= 5:
            cards_of_flush = []
            color_of_flush = max(Counter(suits).items(), key=operator.itemgetter(1))[0]
            for i in self.cards:
                if i.color == color_of_flush:
                    cards_of_flush.append(i)
            return True, cards_of_flush
        else:
            return False, -1

    def check_straight(self, straight_flush = False):
        hand = self.cards
        hand.sort(key = lambda x : x.number)
        straight = False
        count = 1
        cards_of_straight = ()
        cards_of_straight += (hand[0],)
        for _index in range(len(hand)-1):
            if hand[_index].number + 1 == hand[_index+1].number:
                count +=1
                cards_of_straight += (hand[_index+1],)
            elif hand[_index].number == hand[_index+1].number:
                cards_of_straight += (hand[_index+1],)
            elif not straight:
                count = 0
                cards_of_straight = ()
            if count == 5:
                straight = True
        if straight:
            if straight_flush:
                return True, cards_of_straight
            else:
                return True, max(x.number for x in cards_of_straight)
        else:
            return False, -1

    def check_three_of_a_kind(self):
        values = [i.number for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        appearances = sorted(value_counts.values())
        if appearances[-1]>= 3:
            triple_candidates = {k: v for k, v in value_counts.items() if v >=3}
            max_triple = max(Counter(triple_candidates).items(), key=operator.itemgetter(0))[0]
            return True, max_triple
        else:
            return False, -1

    def check_two_pairs(self):
        values = [i.number for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        appearances = sorted(value_counts.values())
        if appearances[-1]>= 2 and appearances[-2]>=2:
            first_pair_candidates = {k: v for k, v in value_counts.items() if v >=2}
            max_first_pair = max(Counter(first_pair_candidates).items(), key=operator.itemgetter(0))[0]
            second_pair_candidates = {k: v for k, v in value_counts.items() if v >=2 and k != max_first_pair}
            max_second_pair = max(Counter(second_pair_candidates).items(), key=operator.itemgetter(0))[0]
            return True, (max_first_pair, max_second_pair)
        return False, -1

    def check_one_pair(self):
        values = [i.number for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        appearances = sorted(value_counts.values())
        if appearances[-1]>= 2:
            pair_candidates = {k: v for k, v in value_counts.items() if v >=2}
            max_pair = max(Counter(pair_candidates).items(), key=operator.itemgetter(0))[0]
            return True, max_pair
        else:
            return False, -1

    def simulate(self, n_iter = 100):
        '''Simulate n_iter games and returns the win rate of the hand'''
        # start = time.time()
        colors = range(4)
        numbers = range(8)
        all_cards = [Card(b, a) for a in numbers for b in colors] #All existing cards
        for card in self.cards:
            all_cards.remove(card)

        n_cards_to_draw = 9 - len(self.cards)
        my_hand_checked = False
        if len(self.cards) >= 7: #my_hand is already determined, no need to iterate
            my_hand, my_cards = FullHand(self.cards[:7]).check_hand_smart()
            my_hand_checked = True
        n_victory = 0
        n_draw = 0
        combinations = list(t.combinations(all_cards, n_cards_to_draw))

        for _iter in range(n_iter):
            random.shuffle(combinations)
            drawn_cards = FullHand(list(combinations[0]))
            personnal_cards = FullHand(self.cards[:2])
            board_cards = FullHand(self.cards[2:] + drawn_cards.cards[:-2])
            assert len(board_cards.cards) == 5, "board should have 5 cards, but has " + str(len(board_cards)) + " cards"
            opponent_cards = FullHand(drawn_cards.cards[-2:])
            if not my_hand_checked:
                my_hand, my_cards = (personnal_cards + board_cards).check_hand_smart()
            adversary_hand, adversary_cards = (opponent_cards + board_cards).check_hand_smart(my_hand = my_hand)

            # end = time.time()
            # print("time elapsed: {}s".format(end - start))

            if (my_hand > adversary_hand):
                n_victory += 1
            elif my_hand == adversary_hand and (my_hand == 7 or my_hand == 3): #Full house or double pairs
                if my_cards[0] > adversary_cards[0]:
                    n_victory += 1
                elif my_cards[0] == adversary_cards[0] and my_cards[1] > adversary_cards[1]:
                    n_victory += 1
                elif my_cards[0] == adversary_cards[0] and my_cards[1] == adversary_cards[1]:
                    n_draw += 1
            elif my_hand == adversary_hand:
                if my_cards > adversary_cards:
                    n_victory += 1
                elif my_cards == adversary_cards:
                    n_draw += 1
        if n_iter != n_draw:
            return n_victory/(n_iter - n_draw)
        else:
            return 0.5
