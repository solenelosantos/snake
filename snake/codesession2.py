import pygame
import abc

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300
DEFAULT_PIXEL= 22
SNAKE_POSITION = [10,5]

def snake():
    args=lignecommande()
    pygame.init()

    screen = pygame.display.set_mode( (args.width, args.height) )

    clock = pygame.time.Clock()
   
    score=0
    pygame.display.set_caption(f"Snake Game - Score: {score}")

    screen.fill( (255, 255, 255) )
    board= Board(screen= screen, tile_size= DEFAULT_PIXEL)
    checkerboard= Checkerboard(args.width, args.height, args.pixel)
    snake =Snake()
    fruit=Fruit()
    board.add_object(checkerboard, snake, fruit)


    Flag=True

    while Flag:

        clock.tick(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    Flag=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Flag= False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')

        
        
        snake.move(screen)
    
        board.draw

        if snake._position[0] == fruit._position:
            snake._position.append(snake._position[-1]) #le serpent grandit
            score += 1
            pygame.display.set_caption(f"Snake Game - Score: {score}")
            fruit.relocate()
    
        pygame.display.update()

import argparse

def lignecommande():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, help="columns number", default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height', type=int, help= "ligns number", default=DEFAULT_HEIGHT)
    parser.add_argument('-p', '--pixel', type=int, help="pixel", default=DEFAULT_PIXEL)
    args = parser.parse_args()
    return args

# La fonction lignecommande permet de définir des lignes de commande. 
# args est un attribut=> Args. contient width et height.
# Pour changer la taille de notre écran => poetry run snake -W 50 -H 50 => cela définit la taille et la largeur à 50 et 50.


def damier(screen, args):
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
        
def starting_position(screen, position, args):
    vert=(0,250,0)
    p=args.pixel
    ligne_t, colonne_t = position[0], position[1]
    snake= pygame.Rect(colonne_t*p, ligne_t*p, 3*p, 1*p)
    pygame.draw.rect(screen,vert, snake)

# Nous définissons une fonction starting_position qui affiche le serpent vert en position initiale.
# On multiplie les grandeurs par la taille des carreaux p. La fonction prend en argument STARTING_POSITION qui est une variable globale définie en début de code.
# Ici STARTING_POSITION=[10,5] => 11ème ligne et 6ème colonne.


class Tile:
     
    def __init__(self,row, column):
        self._row= row
        self._column=column
        
    
    def draw(self,screen, tile_size):
        rect=pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)


class Checkerboard(GameObject):
    def __init__(self, width, height):
        self._width= width
        self._height= height
        self._color1= (0,0,0)
        self._color2=(255,255,255)
    
    @property
    def tiles(self):
        for row in range(self._height):
            for column in range (self._width):
                yield tile=Tile(row= row, column= column, color=self._color1 if (row+column)%2==0 else self._color2)

class Snake(GameObject):
    def __init__(self):
        self._color=(0,255,0)
        self._position= [(10,5), (11,5), (12,5)]
        self._direction = "LEFT"

    def move(self,screen):
        
        head_x, head_y= self._position[0]
        if self._direction == "UP":
            new_head= (head_x , head_y -1)
        if self._direction == "DOWN":
            new_head= (head_x , head_y +1)
        if self._direction == "RIGHT":
            new_head= (head_x +1, head_y)
        if self._direction == "LEFT":
            new_head= (head_x -1, head_y)
        
        self._position= [new_head] + self._position
        self._position.pop()

    def change_direction(self, new_direction):
        self._direction= new_direction

    @property
    def tiles(self):
        iter(self._position)

class Fruit(GameObject):

    def __init__(self,position, color):
        self._tiles = [Tile(row=position[0], column= position[1], color= color)]
    
    @property
    def tiles(self):
        iter(self._tiles)
    
    def relocate(self):
        if self._position == (3,3):
            self._position= (13,10)
        elif self._position == (13,10):
            self._position= (3,3)


class Board :
    def __init__(self, screen, tile_size):
        self._screen= screen
        self._tile_size= tile_size
        self._objects=[]

    def draw(self):
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size )

    def add_object(self,gameobject):
        self._objects.append(gameobject)


class GameObject(abc.ABC):
    def __init__(self):
        super().__init__()
        
    @property
    @abc.abstractmethod
    def tiles(self):
        raise NotImplementedError