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

    Flag=True

    while Flag:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    Flag=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Flag= False
    

        checkerboard= Checkerboard((0,0,0), args.height, args.width, args.pixel)
        checkerboard.draw(screen)

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
    def __init__(self, width, height, pixel,color):
        self._width=width
        self._height=height
        self._pixel =pixel
        self._color=color

    def draw(self, screen, rect):
        pygame.draw.rect(screen, self._color, rect)
      
# Vaut mieux passer le screen dans la fonction draw

class Checkerboard:
    def __init__(self, color, height, width, pixel):
        self._color= color
        self._height= height
        self._width= width
        self._pixel =pixel
    
    def draw(self, screen):
        screen.fill( (255, 255, 255) )
        a=0
        for j in range(0, self._width, self._pixel*2):
            for i in range(0, self._height, self._pixel):
                rect = pygame.Rect(j+self._pixel*(a%2), i, self._pixel, self._pixel)
                tile=Tile(self._width, self._height, self._pixel, self._color)
                Tile.draw(screen,rect)
                a+=1
'''
#class Snake:
    def __init__(self, color, snake_position):
        self._color= color
        self._tete_colonne, self._tete_ligne= snake_position

    def draw(self, pixel):
        rect = pygame.Rect(self._tete_colonne*pixel, self._tete_ligne*pixel, 3*pixel, 1*pixel)
        tile= Tile()
'''