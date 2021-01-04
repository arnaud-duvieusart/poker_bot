from .AbstractAgent import AbstractAgent, Move

class MirrorDummy(AbstractAgent):
    
    def act(self, state):
        #Check that the player still in game
        super().act(state)
        
        #Retreive last move bet of the adversary and the last move type
        call_val = 0
        last_move_type = None
        amount = self.money_left
        
        #Inititalisation case
        if state.last_move:
            call_value = state.last_move.call_val + state.last_move.raise_val 
            last_move_type = state.last_move.move_type
        
        #Mirror actions
        if last_move_type == Move.CALL or last_move_type == Move.CALL_ALLIN:
            #case call_value=0
            if self.spend(call_val):
                return Move.Call(call_val)
            else:
                amount = self.money_left
                self.spend(amount)
                return Move.CallAllIn(call_val, call_allin_val=amount) 
                    
        elif last_move_type == Move.RAISE:
            #Can spend we double the raising value
            if self.spend(2*call_value):
                return Move.Raise(call_val, call_val)
            #If not we call with money_left
            else:
                
                if self.spend(call_val):
                    raise_val = amount - call_val
                    return Move.Raise(call_val, raise_val)
                else:
                    return Move.CallAllIn(call_val, call_allin_val=amount) 
                    
        else:
            return Move.Fold()
                    
                
        