import pygame
import abc
import enum

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300
DEFAULT_PIXEL= 22
SNAKE_POSITION = [10,5]

def snake() -> None:
    args=lignecommande()
    pygame.init()

    screen = pygame.display.set_mode( (args.width, args.height) )

    clock = pygame.time.Clock()
   
    score=0
    pygame.display.set_caption(f"Snake Game - Score: {score}")

    screen.fill( (255, 255, 255) )
    board= Board(screen= screen, tile_size= DEFAULT_PIXEL)
    checkerboard= Checkerboard(args.width, args.height)
    snake =Snake()
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
            snake._position.append(snake._position[-1]) #le serpent grandit
            score += 1
            pygame.display.set_caption(f"Snake Game - Score: {score}")
            fruit.relocate()
    
        pygame.display.update()

import argparse
from typing import NoReturn

def lignecommande():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, help="columns number", default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height', type=int, help= "ligns number", default=DEFAULT_HEIGHT)
    parser.add_argument('-p', '--pixel', type=int, help="pixel", default=DEFAULT_PIXEL)
    return parser.parse_args()

# La fonction lignecommande permet de définir des lignes de commande. 
# args est un attribut=> Args. contient width et height.
# Pour changer la taille de notre écran => poetry run snake -W 50 -H 50 => cela définit la taille et la largeur à 50 et 50.


def damier(screen, args) -> None:
    w,h,p =args.width, args.height, args.pixel
    noir = (0, 0, 0)
    a=0
    for j in range(0, w, p*2):
        for i in range(0, h, p):
            rect = pygame.Rect(j+p*(a%2), i, p, p)
            pygame.draw.rect(screen, noir, rect)
            a+=1

# Nous utilisons des boucles for pour parcourir l'écran blanc et dessiner les carreaux un à un.
# Pour introduire le décalage de carreaux, on utilise la variable a qui change de parité à chaque nouvelle ligne dessinée.
        
def starting_position(screen, position, args) -> None:  
    vert=(0,250,0)
    p=args.pixel
    ligne_t, colonne_t = position[0], position[1]
    snake= pygame.Rect(colonne_t*p, ligne_t*p, 3*p, 1*p)
    pygame.draw.rect(screen,vert, snake)

# Nous définissons une fonction starting_position qui affiche le serpent vert en position initiale.
# On multiplie les grandeurs par la taille des carreaux p. La fonction prend en argument STARTING_POSITION qui est une variable globale définie en début de code.
# Ici STARTING_POSITION=[10,5] => 11ème ligne et 6ème colonne.
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

class Board (Subject, Observer) : # subject car le Board reçoit aussi des infos des objects. 
    def __init__(self, screen, tile_size, nb_rows, nb_cols) -> None:
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

    def remove_object(self, gameobject)
        gameobject.detach_obs(self) # le board n'est plus l'observateur de l'object.
        self._object.remove(gameobject)

    def create_fruit(self)-> Fruit:
        fruit = None
        while fruit is None or not self.detect_collision(fruit) is None:
            fruit= Fruit (color= pygame.Color("red"), col= rd.randint(0, self._nb_cols=1), row= rd.randint(0, self._nb_cols=1))
        
    def detect_collision(self, obj: GameObject):
        for o in self._objects:
            if o != obj and not o.background and o in obj : #opérateur in définit par contains dans GameObject
                return o
        return None
    
    def notify_object_moved(self, obj: GameObject)-> None:
        o=self.detect_collision(obj)
        if not o is None:
                obj.notify_collision(o)

    def notify_object_eaten(self, obj: GameObject)-> None:
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

    def __contains__(self, obj :Object)-> bool:
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

    def __init__(self, tiles, direction) -> None:
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
        """Move the snake one tile."""
        self._tiles.insert(0, self._tiles[0] + self._direction)
        self._tiles.pop()
        """Notify observers"""
        for obs in self.observers:
            obs.notify_object_moved(self) # On previent tous les observeurs que le snake a bougé.
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
            self._size+=1 #On fait en dur, on pourrait généraliser pour ajouter plus de fruits
            for obs in self._observers:
                obs.notify_object_eaten(obj)

class Fruit(GameObject):

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

