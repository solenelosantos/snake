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

    @staticmethod
    def load(filename: str = "high_scores.yaml") -> "Scores":
        """Load scores from a YAML file or create a file with default scores if it doesn't exist."""
        try:
            with open(filename, "r") as f:
                data = yaml.safe_load(f)
                if not data or 'scores' not in data:  # If the file is empty or malformed
                    print("No valid scores found in file, creating a new file with default scores.")  # Debug
                    return Scores.default(max_scores=5)
                max_scores = data.get("max_scores", 5)
                scores = [
                    Score(score=item["score"], name=item["name"])
                    for item in data.get("scores", [])
                ]
                return Scores(max_scores, scores)
        except FileNotFoundError:
            print(f"File {filename} not found, creating a new file with default scores.")  # Debug
            # If the file doesn't exist, create one with default scores
            return Scores.default(max_scores=5)
        
    @staticmethod
    def default(max_scores: int) -> "Scores":
        """Return a default instance with predefined scores."""
        return Scores(
            max_scores,
            [
                Score(score=-1, name="Joe"),
                Score(score=8, name="Jack"),
                Score(score=0, name="Averell"),
                Score(score=6, name="William"),
            ],
        )


