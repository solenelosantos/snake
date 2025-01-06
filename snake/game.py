import pygame
import re


from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import GameOver, ColorError, IntRangeError
from .fruit import Fruit
from .snake import Snake


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

            if snake._position[0] == fruit._position:
                snake._position.append(snake._position[-1]) #the snake grow
                score += 1
                pygame.display.set_caption(f"Snake Game - Score: {score}")
                fruit.relocate()
            pygame.display.update()
            

        pygame.quit()
        
    
    except GameOver:
        pygame.quit()

import argparse
from typing import NoReturn


def lignecommande():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, help="columns number", default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height', type=int, help= "ligns number", default=DEFAULT_HEIGHT)
    parser.add_argument('-p', '--pixel', type=int, help="pixel", default=DEFAULT_PIXEL)
    parser.add_argument('--fps', '--framepersecond', type=int, help= "number of frames per second", default=10)
    parser.add_argument('--fc', "--fruit_color", type=str, help= "color of the fruit", default= '#ff0000' )
    parser.add_argument('--hc', '--snake_head_color', type=str, help="color of the head's snake", default='#ffffff')
    parser.add_argument('--bc', '--snake_body_color', type=str, help="color of the body's snake", default='00ff00')
    args=parser.parse_args()

    if not (FPS_MIN <= args.fps <= FPS_MAX) :
        raise IntRangeError ('fps', args.fps, FPS_MIN, FPS_MAX)
    if not (HEIGHT_MIN <= args.height <= HEIGHT_MAX) :
        raise IntRangeError ('height', args.height, HEIGHT_MIN, HEIGHT_MAX)
    #check argument
    if not re.match(r"#[0-9A-Fa-f]{6}$", args.fruit_color):
        raise ColorError(args.fruit_color, "--fruit_color")
    if not re.match(r"#[0-9A-Fa-f]{6}$", args.snake_head_color):
        raise ColorError(args.snake_head_color, "--snake_head_color")
    if not re.match(r"#[0-9A-Fa-f]{6}$", args.snake_body_color):
        raise ColorError(args.snake_body_color, "--snake_body_color")
    return args
