from .AbstractAgent import AbstractAgent, Move

class CallDummy(AbstractAgent):
    
    def act(self, state):
        #Check that the player still in game
        super().act(state)
        
        #Retreive last move bet of the adversary
        call_val = 0
        if state.last_move:
            call_val = state.last_move.call_val + state.last_move.raise_val
        
        # If we can, we call
        if self.spend(call_val):
            return Move.Call(call_val)
        else:
            amount = self.money_left
            self.spend(amount)
            return Move.CallAllIn(call_val, call_allin_val=amount)

        