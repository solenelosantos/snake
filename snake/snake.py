

import pygame
import typing
import random

from snake.gameobject import GameObject
from snake.tile import Tile
from snake.dir import Dir
from snake.exceptions import GameOver
from snake.fruit import Fruit



class Snake(GameObject):
    """Class used to represent the snake."""

    def __init__(self, tiles: list[Tile], direction: Dir, *,
                 gameover_on_exit: bool = False) -> None:
        """Object initialization."""
        super().__init__()
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
    def length(self) -> int:
        """Snake length."""
        return self._length
    
    @property
    def dir(self) -> Dir:
        """Snake direction."""
        return self._dir

    @dir.setter
    def dir(self, direction: Dir) -> None:
        self._dir= direction

    def move(self) -> None:
        new_head =self._tiles[0] + self._dir
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
        if self._length < len(self._tiles):
            self._tiles = self._tiles[:self._length]

    @property
    def tiles(self) -> typing.Iterator[Tile]:
        """Iterator on the tiles."""
        return iter(self._tiles)

    def notify_collision (self, obj : GameObject)-> None:
        if isinstance(obj, Fruit):
            self._length+=1 #we can generalize to add more fruits.
            for obs in self._observers:
                obs.notify_object_eaten(obj)