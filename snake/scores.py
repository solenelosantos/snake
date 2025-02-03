from snake.score import Score
import typing
import yaml
from pathlib import Path

class Scores:
    def __init__(self,max_scores :int, scores: list[Score])-> None:
        self._max_scores= max_scores
        self._scores= sorted(scores, reverse= True)[:self._max_scores]

    @classmethod
    def default(cls, max_scores:int)-> "Scores":
        return cls(max_scores, [Score(100, 'Joe'), Score(80,'Jack'), Score(60, 'William'), Score(40, 'Averell')])
    
    def __iter__(self)-> typing.Iterator[Score]:
        return iter(self._scores)
    
    def is_highscore(self, score_player :int)-> None:
        return len(self._scores)<self._max_scores or score_player>self._scores[-1]
    
    def add_score(self, score :Score) -> None:
        if self.is_highscore(score):
            if len(self._scores) >= self._max_scores:
                self._scores.pop()
                self._scores.append(score)
                self._scores.sort(reverse=True)

    def save(self, scores_file : Path)-> None:
        x=[{"name": s.name, "score": s.score} for s in self]
        with scores_file.open("w") as fd:
            yaml.safe_dump(x, fd)


