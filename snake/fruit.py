import pygame
import typing
import random

from snake.gameobject import GameObject
from snake.tile import Tile


class Fruit(GameObject):
    """Class used to represent the fruit."""

    
    color = pygame.Color("black")

    def __init__(self, tile: Tile) -> None:
        """Object initialization."""
        super().__init__()
        self._tiles = [tile]

    @property
    def tiles(self) -> typing.Iterator[Tile]:
        """
        An iterator on the tiles.

        Note that this object contains only one tile.
        """
        return iter(self._tiles)

    # Create a Fruit at random position on the board
    @classmethod
    def create_random(cls, nb_lines: int, nb_cols: int) -> typing.Self:
        """Create a random fruit."""
        
        random.seed()
        x = random.randint(0, nb_cols - 1)
        y = random.randint(0, nb_lines - 1)
        return cls(Tile(x, y, cls.color))
