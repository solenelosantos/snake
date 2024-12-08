import pygame

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300
DEFAULT_PIXEL= 25
SNAKE_POSITION = [10,5]

def snake():
    args=lignecommande()
    pygame.init()

    screen = pygame.display.set_mode( (args.width, args.height) )

    clock = pygame.time.Clock()

    
    snake =Snake(args)

    Flag=True

    while Flag:

        clock.tick(1)

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
                    
        screen.fill( (255, 255, 255) )
        checkerboard= Checkerboard(args.width, args.height, args.pixel)
        checkerboard.draw(screen)
        snake.move(screen)
        snake.draw(screen)



        #starting_position(screen, SNAKE_POSITION, args)
        
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
     
    def __init__(self,pixel, color):
        self._pixel= pixel
        self._color= color
    
    def draw(self,screen, rect):
        pygame.draw.rect(screen, self._color, rect)


class Checkerboard():
    def __init__(self, width, height, pixel):
        self._width= width
        self._height= height
        self._pixel= pixel
        self._noir= (0,0,0)
    
    def draw(self,screen):
        w,h,p =self._width, self._height, self._pixel 
        a=0
        for j in range(0, w, p*2):
            for i in range(0, h, p):
                rect = pygame.Rect(j+p*(a%2), i, p, p)
                tile=Tile(p,self._noir)
                tile.draw(screen, rect)
                a+=1

class Snake():
    def __init__(self,args):
        self._color=(0,255,0)
        self._position= [(10,5), (11,5), (12,5)]
        self._direction = "LEFT"
        self._pixel= args.pixel

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

    def draw(self,screen):

        for x,y in self._position :
            rect= pygame.Rect(x*self._pixel,y*self._pixel,self._pixel,self._pixel)
            tile=Tile(self._pixel,self._color)
            tile.draw(screen, rect)

    def change_direction(self, new_direction):
        self._direction= new_direction

