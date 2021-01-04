from .AbstractAgent import AbstractAgent, Move

class AggressiveDummy(AbstractAgent):

    def act(self, state):
        super().act(state)

        raise_val = 1000

        # If the position is good
        if self.hand.position(state.board_cards) > 0.5:

            call_val = 0
            if state.last_move:
                
                #call_val = state.last_move.call_val
                call_val = state.last_move.call_val + state.last_move.raise_val

            # If we can, we raise
            if self.spend(call_val + raise_val):
                return Move.Raise(call_val, raise_val)

            # If we can, we call
            if self.spend(call_val):
                return Move.Call(call_val)

            # Otherwise we go all in
            else:
                amount = self.money_left
                self.spend(amount)
                return Move.CallAllIn(call_val, call_allin_val=amount)


        # Else we fold
        else:
            return Move.Fold()
