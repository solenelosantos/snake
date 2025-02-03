from snake.gameobject import GameObject
from snake.tile import Tile


class Checkerboard(GameObject):
    """Class used to represent the Checkerboard."""

    def __init__(self, nb_lines, nb_cols) -> None:
        super().__init__()
        self._width= nb_lines
        self._height= nb_cols
        self._color1= (0,0,0)
        self._color2=(255,255,255)

    @property
    def background(self):
        return True

    @property
    def tiles(self):
        for row in range(self._height):
            for column in range (self._width):
                yield iter(Tile(row= row, column= column, color=self._color1 if (row+column)%2==0 else self._color2))