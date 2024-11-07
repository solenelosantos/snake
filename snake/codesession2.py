import pygame

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300

def snake():
    args=lignecommande()
    pygame.init()

    screen = pygame.display.set_mode( (args.width, args.height) )

    clock = pygame.time.Clock()

    while True:

        clock.tick(1)

        for event in pygame.event.get():
            pass

        screen.fill( (255, 255, 255) )

        pygame.display.update()

import argparse

def lignecommande():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, help="screen width", default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height', type=int, help= "screen height", default=DEFAULT_HEIGHT)
    args = parser.parse_args()
    return args

# La fonction lignecommande permet de définir des lignes de commande. 
# args est un attribut, on met un point. Args. contient width et height.
#Maintenant, pour changer la taille de notre écran, on met poetry run snake -W 50 -H 50 => cela définit la taille et la largeur à 50 et 50.
