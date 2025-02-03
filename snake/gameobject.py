import abc
from snake.subject import Subject
from snake.observer import Observer
from typing import NoReturn

class GameObject(Subject, Observer): #il vaut mieux mettre Subject en premier. Subject=class, Observeur= interface
    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> NoReturn: 
        raise NotImplementedError

    def background(self)-> bool:
        return False #by default, a gameobject is not a background

    def __contains__(self, obj :"GameObject")-> bool:
        """Check if an game object intersects with another."""
        if not isinstance(obj, GameObject):
            return False
        return any(t in self.tiles for t in obj.tiles)