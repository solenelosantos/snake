


class Score:
    def __init__(self, score : int, name : str):
        self._score= score
        self._name= name[:MAX_LENGHT]

    @property
    def name(self)-> str:
        return self._name
    
    @property
    def score(self)-> int:
        return self._score 
    
    def __it__(self, other :object)-> bool:
        return isinstance(object, Score) and self._score< other._score