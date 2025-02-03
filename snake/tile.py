import pygame

from snake.dir import Dir

class Tile:
    
    def __init__(self, x: int, y: int, color: pygame.Color) -> None:
        """Object initialization."""
        self._x = x # Column index
        self._y = y # Line index
        self._color = color
        
    @property
    def x(self) -> int:
        """The x coordinate (i.e.: column index) of the tile."""
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        """Set the x coordinate."""
        self._x = value

    @property
    def y(self) -> int:
        """The y coordinate (i.e.: line index) of the tile."""
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        """Set the y coordinate."""
        self._y = value

    @property
    def color(self) -> pygame.Color:
        """The color of the tile."""
        return self._color

    @color.setter
    def color(self, color: pygame.Color) -> None:
        """Change the color of the tile."""
        self._color = color

    def __add__(self, other):
        if not isinstance(other,Dir):
            raise ValueError('Type is wrong')
        return Tile (self._row + other.value[1], self._column +other.value[0], self._color)
    
    def __eq__(self, other: object) -> bool:
        """
        Check if two tiles are equal.

        Compare the x and y coordinates.
        """
        if isinstance(other, Tile):
            return self._x == other._x and self._y == other._y
        return False

    def __add__(self, other: object) -> "Tile":
        """Add two tiles together or a tile with a direction."""
        if isinstance(other, (Tile, Dir)):
            return Tile(x = self.x + other.x, y = self.y + other.y,
                        color = self.color)
        msg = f"Wrong object type {type(object)}."
        raise ValueError(msg)

    def __sub__(self, other: object) -> "Tile":
        """Substract a tile or a direction to this tile."""
        if isinstance(other, (Tile, Dir)):
            return Tile(x = self.x - other.x, y = self.y - other.y,
                        color = self.color)
        msg = f"Wrong object type {type(object)}."
        raise ValueError(msg)

    def draw(self,screen, tile_size) -> None:
        rect=pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)