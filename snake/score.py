
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
    
    
    # Implemente the comparaison operators to use the function sort in the lists
    def __gt__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score > other._score

    def __lt__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score < other._score

    def __eq__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score == other._score

    def __ge__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score >= other._score

    def __le__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score <= other._score

    def __ne__(self, other : object) -> bool :
        """Define the comparaison operator."""
        return isinstance(other, Score) and self._score != other._score
