import pygame
import re
import importlib.resources
import time

from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import SnakeException, GameOver, ColorError, IntRangeError
from .fruit import Fruit
from .snake import Snake
from.lignecommande import lignecommande, DEFAULT_HEIGHT, DEFAULT_PIXEL, DEFAULT_WIDTH
from .state import State
from .scores import Scores
from .score import Score

# Constants
SK_START_LENGTH = 3

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

class Game:

    def __init__(self, width:int, height:int, tile_size:int,fps: int,
                 fruit_color: pygame.Color,
                 snake_head_color: pygame.Color,
                 snake_body_color: pygame.Color,):
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._fps = fps
        self._fruit_color = fruit_color
        self._snake_head_color = snake_head_color
        self._snake_body_color = snake_body_color
        self._snake= None

    def _init(self) -> None:
        """Initialize the game."""

        # Upload font
        with importlib.resources.path("snake", "DejaVuSansMono-Bold.ttf") as f:
            self._fontscore= pygame.font.Font(f,32)
            self._fontgameover= pygame.font.Font(f,64)
            self._highscore= pygame.font.Font(f,32)


        # Create a display screen
        screen_size = (self._width * self._tile_size,
                       self._height * self._tile_size)
        self._screen = pygame.display.set_mode(screen_size)

        # Create the clock
        self._clock = pygame.time.Clock()

        # Create the main board
        self._board = Board(screen = self._screen,
                            nb_lines = self._height,
                            nb_cols = self._width,
                            tile_size = self._tile_size)

        # Create checkerboard
        self._checkerboard = Checkerboard(nb_lines = self._height,
                                          nb_cols = self._width)
        self._board.add_object(self._checkerboard)

        # Create scores:
        self._scores= Scores.default(5)

        # Create snake
        self._resetsnake()
        

        # Create fruit
        Fruit.color = self._fruit_color
        self._board.create_fruit()


    def _resetsnake(self):
        
        if self._snake is not None:
            self._board.remove_object_object(self._snake)
            self._board.detach_obs(self._snake)
        self._snake = Snake.create_random(
                nb_lines = self._height,
                nb_cols = self._width,
                length = SK_START_LENGTH,
                head_color = self._snake_head_color,
                body_color = self._snake_body_color,
                gameover_on_exit = self._gameover_on_exit,
                )
        self._board.add_object(self._snake)
        self._board.attach_obs(self._snake)

    def _process_scores_event(self,event):
        if event.type== pygame.KEYDOWN and event.key== pygame.K_SPACE:
            self._state= State.PLAY

    def _process_play_event(self,event):
        # Key press
        if event.type == pygame.KEYDOWN:
            # Quit
            match event.key:
                case pygame.K_UP:
                    self._snake.dir = Dir.UP
                case pygame.K_DOWN:
                    self._snake.dir = Dir.DOWN
                case pygame.K_LEFT:
                    self._snake.dir = Dir.LEFT
                case pygame.K_RIGHT:
                    self._snake.dir = Dir.RIGHT

    def _process_events(self) -> None:
        """Process pygame events."""
        # Loop on all events
        for event in pygame.event.get():

            match self._state:
                case State.SCORES :
                    self._process_scores_events(event)
                case State.PLAY:
                    self._process_play_events(event)
            # Closing window (Mouse click on cross icon or OS keyboard shortcut)
            if event.type == pygame.QUIT:
                self._state= State.QUIT

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self._state= State.QUIT


    def _draw_gameover():
        text_gameover = self._fontgameover.render("Game Over", True, pygame.Color("red"))
        x, y = 80, 160 # Define the position where to write text.
        self._screen.blit(text_gameover, (x, y))
    
    def _draw_score():
        x,y= 80,10
        for score in self._scores:
            text_score = self._fontscore.render({score.name}.ljust(Score.MAX_LENGHT)+f" {score.score: .>8}", True, pygame.Color("red"))
            self._screen.blit(text_score, (x, y))
            y+=32
        
    def start(self) -> None:
        """Start the game."""
        # Initialize pygame
        pygame.init()

    
        # Initialize game
        self._init()

        # Start pygame loop
        self._state= State.PLAY

        while self._state != State.QUIT:

            # Wait 1/FPS second
            self._clock.tick(self._fps)

            # Listen for events
            self._process_events()

            try :
                # Update objects
                if self._state== State.PLAY:
                    self._snake.move()

            except GameOver:
                self._state= State.GAME_OVER
                cpt= self._fps
                self._resetsnake()

            # Draw
            self._board.draw()


            match self._state:
                case State.GAME_OVER:
                    self._draw_gameover()
                    cpt-=1
                    if cpt ==0 :
                        score= self._snake.score
                        self._reset_snake()
                        if self._scores.ishighscore(score):
                            self._state= State.INPUT_NAME
                        else : 
                            self._state= State.SCORES
                case State.SCORES :
                    self._draw_score()
            

            # Display
            pygame.display.update()

        # Terminate pygame
        pygame.quit()