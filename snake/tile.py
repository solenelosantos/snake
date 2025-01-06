import pygame

from .dir import Dir

class Tile:
    def __init__(self,row, column,color) -> None:
        self._row= row
        self._column=column
        self._color=color

    def draw(self,screen, tile_size) -> None:
        rect=pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

    def __add__(self, other):
        if not isinstance(other,Dir):
            raise ValueError('Type is wrong')
        return Tile (self._row + other.value[1], self._column +other.value[0], self._color)