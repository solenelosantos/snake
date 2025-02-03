import typing

from snake.gameobject import GameObject
from snake.tile import Tile


class Checkerboard(GameObject):
    """Class used to represent the Checkerboard."""

    def __init__(self, nb_lines : int, nb_cols: int) -> None:
        """Object initialization."""
        super().__init__()
        self._width= nb_lines
        self._height= nb_cols
        self._color1= (0,0,0)
        self._color2=(255,255,255)

    
    def is_background(self)-> bool:
        """Test if this object is a background object."""
        return True

    @property
    def tiles(self)-> typing.Iterator[Tile]:
        """Tiles generator."""
        for i in range(self._height):
            for j in range (self._width):
                yield Tile(x= i, y= j, color=self._color1 if (i+j)%2==0 else self._color2)