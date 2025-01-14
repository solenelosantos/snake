
MAX_LENGTH=8

class Score:
    def __init__(self, score : int, name : str):
        self._score= score
        self._name= name

    @property
    def name(self)-> str:
        return self._name
    
    @name.setter
    def name(self, n:str) -> None:
        """Modify the name."""
        self._name= n[:self.MAX_lENGTH]

    @property
    def score(self)-> int:
        return self._score 
    
    def __it__(self, other :object)-> bool:
        return isinstance(other, Score) and self._score< other._score