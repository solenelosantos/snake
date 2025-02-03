# Standard
import abc
import typing

# First party
from .observer import Observer
from .subject import Subject
from .tile import Tile

class GameObject(Subject, Observer):
    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> typing.Iterator[Tile]:
        """The tiles of the object."""
        raise NotImplementedError

    def background(self)-> bool:
        """Tell if this object is a background object."""
        return False #by default, a gameobject is not a background

    def __contains__(self, obj :"GameObject")-> bool:
        """Check if an game object intersects with another."""
        if not isinstance(obj, GameObject):
            return False
        return any(t in self.tiles for t in obj.tiles)