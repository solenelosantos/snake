import pygame
import abc
import enum
import random as rd
import re

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300
DEFAULT_PIXEL= 22
SNAKE_POSITION = [10,5]
FPS_MIN=5
FPS_MAX=25
HEIGHT_MIN=200
HEIGHT_MAX=400


def snake() -> None:
    args=lignecommande()
    pygame.init()
    try :
    screen = pygame.display.set_mode( (args.width, args.height) )

    clock = pygame.time.Clock()

    score=0
    pygame.display.set_caption(f"Snake Game - Score: {score}")

    screen.fill( (255, 255, 255) )
    board= Board(screen= screen, tile_size= DEFAULT_PIXEL, nb_rows=DEFAULT_HEIGHT//DEFAULT_PIXEL, nb_cols=DEFAULT_WIDTH//DEFAULT_PIXEL)
    checkerboard= Checkerboard(args.width, args.height)
    snake =Snake([(10,5),(11,5),(12,5)], Dir.LEFT)
    fruit=Fruit(position=(3,3), color=(0,255,0))
    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    Flag=True

    while Flag:

        clock.tick(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    Flag=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Flag= False

                elif event.key == pygame.K_UP:
                    snake.dir= Dir.UP

                elif event.key == pygame.K_DOWN:
                    snake.dir= Dir.DOWN

                elif event.key == pygame.K_RIGHT:
                    snake.dir= Dir.RIGHT

                elif event.key == pygame.K_LEFT:
                    snake.dir= Dir.LEFT


        snake.move()

        board.draw

        if snake._position[0] == fruit._position:
            snake._position.append(snake._position[-1]) #the snake grow
            score += 1
            pygame.display.set_caption(f"Snake Game - Score: {score}")
            fruit.relocate()
        pygame.display.update()

    except GameOver:
        pygame.quit()

import argparse
from typing import NoReturn


class SnakeException (Exception):
    def __init__(self, message :str)->None:
        super().__init__(message)

class SnakeError( SnakeException):
    def __init__(self, message :str)->None:
        super().__init__(message)

class IntRangeError(SnakeError):
    def __init__(self, name: str, value:int, Vmin: int, Vmax: int)-> None:
        super().__init__(f"Value {value} of {lignecommande} is out of allowed range [{Vmin}-{Vmax}].")

class ColorError(SnakeError):
    def __init__(self, bad_color: str, name :str):
        super().__init__(f"Wrong color {bad_color} for argument name.")

class GameOver (SnakeException):
    def __init__(self):
        super().__init__(f'Game over')


def lignecommande():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, help="columns number", default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height', type=int, help= "ligns number", default=DEFAULT_HEIGHT)
    parser.add_argument('-p', '--pixel', type=int, help="pixel", default=DEFAULT_PIXEL)
    parser.add_argument('--fps', '--framepersecond', type=int, help= "number of frames per second", default=10)
    parser.add_argument('-c', "--fruit_color", type=str, help= "color of the fruit", default= 'ff0000' )
    args=parser.parse_args()

    if not (FPS_MIN <= args.fps <= FPS_MAX) :
        raise IntRangeError ('fps', args.fps, FPS_MIN, FPS_MAX)
    if not (HEIGHT_MIN <= args.height <= HEIGHT_MAX) :
        raise IntRangeError ('height', args.height, HEIGHT_MIN, HEIGHT_MAX)
    #check argument
    if not re.match(r"#[0-9A-Fa-f]{6}$", args.fruit_color):
        raise ColorError(args.fruit_color, '--fruit_color')
    

    return args

def damier(screen, args) -> None:
    w,h,p =args.width, args.height, args.pixel
    noir = (0, 0, 0)
    a=0
    for j in range(0, w, p*2):
        for i in range(0, h, p):
            rect = pygame.Rect(j+p*(a%2), i, p, p)
            pygame.draw.rect(screen, noir, rect)
            a+=1

def starting_position(screen, position, args) -> None:  
    vert=(0,250,0)
    p=args.pixel
    ligne_t, colonne_t = position[0], position[1]
    snake= pygame.Rect(colonne_t*p, ligne_t*p, 3*p, 1*p)
    pygame.draw.rect(screen,vert, snake)


class Observer(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    def notify_object_eaten(self, obj: "GameObject") -> None:
        pass
# C'est le snake qui appelle cette méthode
    def notify_object_moved(self, obj: "GameObject") -> None:
        pass
# C'est le Board qui appelle le fruit et le snake.
    def notify_collision(self, obj: "GameObject" ) -> None:
        pass

class Subject(abc.ABC):

    def __init__(self) -> None:
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        print(f"Attach {obs} as observer of {self}.")
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        print(f"Detach observer {obs} from {self}.")
        self._observers.remove(obs)

class Board (Subject, Observer) : # subject car le Board reçoit aussi des infos des objets. 
    def __init__(self, screen, tile_size, nb_rows, nb_cols) -> None:
        super().__init__()
        self._screen= screen
        self._tile_size= tile_size
        self._objects=[]
        self._nb_rows= nb_rows
        self._nb_cols= nb_cols

    def draw(self) -> None:
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size )

    def add_object(self,gameobject):
        self._objects.append(gameobject)
        gameobject.attach_obs(self) #permet au board de devenir l'observeur des objects ajoutés.

    def remove_object(self, gameobject):
        gameobject.detach_obs(self) # le board n'est plus l'observateur de l'object.
        self._object.remove(gameobject)

    def create_fruit(self)-> "Fruit":
        fruit = None
        while fruit is None or not self.detect_collision(fruit) is None:
            fruit= Fruit (color= pygame.Color("red"), col= rd.randint(0, 1), row= rd.randint(0, 1))

    def detect_collision(self, obj: "GameObject"):
        for o in self._objects:
            if o != obj and not o.background and o in obj : #opérateur in définit par contains dans GameObject
                return o
        return None

    def notify_object_moved(self, obj: "GameObject")-> None:
        o=self.detect_collision(obj)
        if not o is None:
                obj.notify_collision(o)

    def notify_object_eaten(self, obj: "GameObject")-> None:
        self.remove_object(obj) # Remove the fruit eaten
        self.create_fruit()

class GameObject(Subject, Observer): #il vaut mieux mettre Subject en premier. Subject=class, Observeur= interface
    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> NoReturn:
        raise NotImplementedError

    @property
    def background(self):
        return False #by default, a gameobject is not a background

    def __contains__(self, obj :"GameObject")-> bool:
        if isinstance(obj, GameObject):
            return any(t in obj.tiles for t in self.tiles)
        return False


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

class Checkerboard(GameObject):
    """Class used to represent the snake."""

    def __init__(self, width, height) -> None:
        super().__init__()
        self._width= width
        self._height= height
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

class Snake(GameObject):
    """Class used to represent the snake."""

    def __init__(self, tiles: list[Tile], direction) -> None:
        super().__init__()
        self._direction = direction
        self._tiles:list[Tile] =tiles

    @classmethod
    def create_from_pos(cls, color, row, column, direction, size):
        tiles= [Tile(row,column+p, color) for p in range (size)]
        return Snake (tiles, direction = direction)

    def __len__(self):
        return len(self._tiles)

    def move(self) -> None:
        self
        if self._tiles[0] 
            raise GameOver
        """Move the snake one tile."""
        self._tiles.insert(0, self._tiles[0] + self.dir)
        self._tiles.pop()
        """Notify observers"""
        for obs in self.observers:
            obs.notify_object_moved(self) # notify observers the snake moved.
        """shrink"""
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
        iter(self._position)

    def notify_collision (self, obj : GameObject)-> None:
        if isinstance(obj, Fruit):
            self._size+=1 #we can generalize to add more fruits.
            for obs in self._observers:
                obs.notify_object_eaten(obj)

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

class Dir(enum.Enum):
    UP=(0,-1)
    DOWN=(0,1)
    RIGHT=(1,0)
    LEFT=(-1,0)

