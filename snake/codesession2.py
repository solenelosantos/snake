import pygame

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300
DEFAULT_PIXEL= 10

def snake():
    args=lignecommande()
    pygame.init()

    screen = pygame.display.set_mode( (args.width, args.height) )

    clock = pygame.time.Clock()

    Flag=True
    print ('test')
    while Flag:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    Flag=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Flag= False
    

        screen.fill( (255, 255, 255) )
        damier(screen)

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
# args est un attribut, on met un point. Args. contient width et height.
#Maintenant, pour changer la taille de notre écran, on met poetry run snake -W 50 -H 50 => cela définit la taille et la largeur à 50 et 50.

def damier(screen):
    noir = (0, 0, 0) 
    for i in range(0,400,10):
        for j in range(0,300, 10):
            rect = pygame.Rect(i, j, 10, 10)
            pygame.draw.rect(screen, noir, rect)