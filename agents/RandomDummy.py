import random as rd
from .AbstractAgent import AbstractAgent, Move

class RandomDummy(AbstractAgent):
    
    def act(self, state):
        #Check that the player still in game
        super().act(state)
        
        #Retreive last move bet of the adversary and the last move type
        call_val = 0
        last_move_type = None
        amount = self.money_left
        
        if state.last_move:
            call_val = state.last_move.call_val + state.last_move.raise_val
            last_move_type = state.last_move.move_type
            
        choice = rd.choice([Move.CALL, Move.RAISE, Move.FOLD])
        
        if choice == Move.CALL:
            if self.spend(call_val):
                return Move.Call(call_val)
            else:
                self.spend(amount)
                return Move.CallAllIn(call_val, call_all_in_val=amount)
        
        elif choice == Move.Raise:
            #Deal with different cases: 
            # Double the raising value
            if last_move_type == Move.Raise:
                if self.spend(2*call_val):
                    return Move.Raise(call_val, call_val)
                else:  
                    self.spend(amount)
                    raise_val = amount - call_val
                    return Move.Raise(call_val, raise_val)
            else:
                raise_val = andom.randint(1,self.money_left)
                if self.spend(raise_val):
                    return Move.Raise(raise_val)
        
        else:
            return Move.Fold()
            
            
        