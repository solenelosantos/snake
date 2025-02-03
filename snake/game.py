import pygame
import importlib.resources
from pathlib import Path

from snake.board import Board
from snake.checkerboard import Checkerboard
from snake.dir import Dir
from snake.exceptions import GameOver
from snake.fruit import Fruit
from snake.snake import Snake
from snake.lignecommande import lignecommande, DEFAULT_HEIGHT, DEFAULT_PIXEL, DEFAULT_WIDTH
from snake.state import State
from snake.scores import Scores
from snake.score import Score

# Constants
SK_START_LENGTH = 3

class Game:

    def __init__(self, width:int, height:int, tile_size:int,fps: int,
                 fruit_color: pygame.Color,
                 snake_head_color: pygame.Color,
                 snake_body_color: pygame.Color, scores_file : Path, gameover_on_exit):
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._fps = fps
        self._fruit_color = fruit_color
        self._snake_head_color = snake_head_color
        self._snake_body_color = snake_body_color
        self._snake= None
        self._new_high_score = None | Score
        self._scores_file= scores_file
        self._gameover_on_exit = gameover_on_exit

    def _reset_snake(self) -> None:
        """Reset the snake."""
        if self._snake is not None:
            self._board.detach_obs(self._snake)
            self._board.remove_object(self._snake)
        self._snake = Snake.create_random(
                nb_lines=self._height,
                nb_cols=self._width,
                length=SK_START_LENGTH,
                head_color=self._snake_head_color,
                body_color=self._snake_body_color,
                gameover_on_exit=self._gameover_on_exit,
        )
        self._board.add_object(self._snake)
        self._board.attach_obs(self._snake)

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
                            nb_rows = self._height,
                            nb_cols = self._width,
                            tile_size = self._tile_size)

        # Create checkerboard
        self._checkerboard = Checkerboard(nb_lines = self._height,
                                          nb_cols = self._width)
        self._board.add_object(self._checkerboard)
    
        # Create scores:
        
        self._scores= Scores.default(5)
        self._scores.save(self._scores_file)
        

        # Create snake
        self._reset_snake()
        

        # Create fruit
        Fruit.color = self._fruit_color
        self._board.create_fruit()

    def _drawgameover(self) -> None:
        """Draw the gameover's sentence."""
        text_gameover = self._fontgameover.render("GAME OVER", True, pygame.Color("red"))
        x, y = 80, 160  # Define the position where to write text.
        self._screen.blit(text_gameover, (x, y))

    def _draw_scores(self) -> None:
        """Put a highscore's line."""
        x, y = 80, 10  # Define the position where to write text.
        for score in self._scores:
            text_scores = self._fontscore.render(score.name.ljust(Score.MAX_LENGTH) + f" {score.score: >8}", True, pygame.Color("red"))
            self._screen.blit(text_scores, (x, y))
            y += 32
        pygame.display.update()

    def _draw_inputname(self) -> None:
        """Draw the input name screen."""
        text = self._highscore.render(f"Enter your name: {self._new_high_score.name}", True, pygame.Color("red"))
        x, y = 80, 10  # Position of the text
        self._screen.blit(text, (x, y))
        pygame.display.update()

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

    def _process_inputname(self, event: pygame.event.Event) -> None :
        """The player put his/her name in the ranking list of highscores."""
        if self._new_high_score is not None and event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RETURN:  # Validate the name
                self._state = State.SCORES
            elif event.key == pygame.K_BACKSPACE:  # Correct a mistake
                self._new_high_score.name=self._new_high_score.name[:-1]
            else :
                self._new_high_score.name+= event.unicode

    def _process_events(self) -> None:
        """Process pygame events."""
        # Loop on all events
        for event in pygame.event.get():

            match self._state:
                case State.SCORES :
                    self._process_scores_event(event)
                case State.PLAY:
                    self._process_play_event(event)
            # Closing window (Mouse click on cross icon or OS keyboard shortcut)
            if event.type == pygame.QUIT:
                self._state= State.QUIT

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self._state= State.QUIT
        
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
                self._state= State.GAMEOVER
                cpt= self._fps

            # Draw
            self._board.draw()
            match self._state:
                case State.GAMEOVER:
                    self._drawgameover()
                    cpt-= 1
                    if cpt == 0:
                        score = self._snake.score
                        self._reset_snake()
                        if self._scores.is_highscore(score):
                            self._new_high_score = Score(name="", score=score)
                            self._state = State.INPUT_NAME  # Switch to name input state
                        else:
                            self._state = State.SCORES
                case State.SCORES:
                    self._draw_scores()
                case State.INPUT_NAME:
                    self._draw_inputname()
            

            # Display
            pygame.display.update()

        # Terminate pygame
        pygame.quit()