from .AbstractAgent import AbstractAgent, Move

# Always raise until allin or fold we have to choose
class RaiseDummy(AbstractAgent):
    
    def act(self, state):
        #Check that the player still in game
        super().act(state)
        
        #Retreive last move bet of the adversary and the last move type
        call_val = 0
        
        if state.last_move:
            call_val = state.last_move.call_val + state.last_move.raise_val
        
        
        if self.spend(2*call_val):
                return Move.Raise(call_val, call_val)
        else:
            #ALLIN or FOLD ?
            #amount = self.money_left
            #self.spend(amount)
            #eturn Move.CallAllIn(amount)
            return Move.Fold()
