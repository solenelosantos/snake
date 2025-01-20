

import pygame
import typing
import random

from .gameobject import GameObject
from .tile import Tile
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit



class Snake(GameObject):
    """Class used to represent the snake."""

    def __init__(self, tiles: list[Tile], direction: Dir, *,
                 gameover_on_exit: bool = False) -> None:
        """Object initialization."""
        self._tiles = tiles
        self._dir = direction
        self._length = len(tiles)
        self._gameover_on_exit = gameover_on_exit

    # Create a Snake at random position on the board
    @classmethod
    def create_random(cls, nb_lines: int, nb_cols: int, # noqa: PLR0913
                      length: int,
                      *,
                      head_color: pygame.Color,
                      body_color: pygame.Color,
                      gameover_on_exit: bool = False) -> typing.Self:
        """Create a snake and place it randomly on the board."""
        tiles = [] # List of tuples (col_index, line_index)

        # Choose head
        random.seed()
        x = random.randint(length - 1, nb_cols - length)
        y = random.randint(length - 1, nb_lines - length)
        tiles.append(Tile(x, y, head_color))

        # Choose body orientation (i.e.: in which direction the snake will move)
        random.seed()
        snake_dir = random.sample([Dir.LEFT, Dir.RIGHT, Dir.UP, Dir.DOWN], 1)[0]

        # Create body
        while len(tiles) < length:
            tile = tiles[-1] - snake_dir
            tile.color = body_color
            tiles.append(tile)

        return cls(tiles, direction = snake_dir,
                   gameover_on_exit = gameover_on_exit)


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