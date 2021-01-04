from .AbstractAgent import AbstractAgent, Move

#Check everytime and fold otherwise
class CheckFoldDummy(AbstractAgent):
    
    def act(self, state):
        #Check that the player still in game
        super().act(state)
        
        #Retreive last move bet of the adversary and the last move type
        call_val = 0
        
        if state.last_move:
            call_val = state.last_move.call_val + state.last_move.raise_val
        
        #If call value== 0 we call
        if self.spend(call_val):
            return Move.Call(call_val)
        else:
            return Move.Fold()
            