import pygame
import re


from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import SnakeException, GameOver, ColorError, IntRangeError
from .fruit import Fruit
from .snake import Snake
from.lignecommande import lignecommande, DEFAULT_HEIGHT, DEFAULT_PIXEL, DEFAULT_WIDTH



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

