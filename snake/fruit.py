from snake.gameobject import GameObject
from snake.tile import Tile


class Fruit(GameObject):
    """Class used to represent the fruit."""

    def __init__(self,position, color) -> None:
        super().__init__()
        self._tiles = [Tile(row=position[0], column= position[1], color= color)]

    @property
    def tiles(self) -> None:
        iter(self._tiles)

    def relocate(self) -> None:
        if self._position == (3,3):
            self._position= (13,10)
        elif self._position == (13,10):
            self._position= (3,3)