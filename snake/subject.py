import abc
from snake.observer import Observer

class Subject(abc.ABC):

    def __init__(self) -> None:
        super().__init__()
        self._observers = []

    @property
    def observers(self) -> list[Observer]:
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        print(f"Attach {obs} as observer of {self}.")
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        print(f"Detach observer {obs} from {self}.")
        self._observers.remove(obs)