

import pygame
from .game_object import GameObject
from .tile import Tile
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit


class Snake(GameObject):
    """Class used to represent the snake."""

    def __init__(self, tiles: list[Tile], direction : Dir) -> None:
        super().__init__()
        self._direction = direction
        self._tiles:list[Tile] =tiles

    @classmethod
    def create_from_pos(cls, color, row, column, direction, size):
        tiles= [Tile(row,column+p, color) for p in range (size)]
        return Snake (tiles, direction = direction)

    @property
    def dir(self) -> Dir:
        """Snake direction."""
        return self._direction

    @dir.setter
    def dir(self, direction: Dir) -> None:
        self._direction = direction

    def __len__(self):
        return len(self._tiles)

    def move(self) -> None:
        new_head =self._tiles[0] + self._direction.value
        # check if the snake slithers on itself
        if new_head in self._tiles:
            raise GameOver
        # Move the snake one tile
        self._tiles.insert(0, new_head)
        self._tiles.pop()
        # Notify observers the snake moved.
        for obs in self.observers:
            obs.notify_object_moved(self)
        # shrink
        if self._size < len(self._tiles):
            self._tiles = self._tiles[:self._size]

    @property
    def dir(self):
        return self._direction

    @dir.setter
    def dir(self, new_direction) -> None:
        self._direction = new_direction

    @property
    def tiles(self) -> None: 
        iter(self._tiles)

    def notify_collision (self, obj : GameObject)-> None:
        if isinstance(obj, Fruit):
            self._size+=1 #we can generalize to add more fruits.
            for obs in self._observers:
                obs.notify_object_eaten(obj)