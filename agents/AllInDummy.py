from .AbstractAgent import AbstractAgent, Move

class AllInDummy(AbstractAgent):
   
    def act(self, state):
        #Check that the player still in game
        super().act(state)
        call_val = 0
        amount = self.money_left
        
        if state.last_move:
            call_val = state.last_move.call_val + state.last_move.raise_val
            last_move_type = state.last_move.move_type
        
        
        if self.spend(call_val):
            raise_val = amount - call_val
            return Move.Raise(call_val, raise_val)
        else:
            return Move.CallAllIn(call_val, call_allin_val=amount)
        
            
        