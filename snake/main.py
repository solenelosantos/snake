import sys

# First party
from .lignecommande import lignecommande
from .exceptions import SnakeError
from .game import Game


def main() -> None:

    try:
        # Read command line arguments
        args = lignecommande()

        # Start game
        Game(width = args.width, height = args.height,
             tile_size = args.tile_size, fps = args.fps,
             fruit_color = args.fruit_color,
             snake_head_color = args.snake_head_color,
             snake_body_color = args.snake_body_color,
             gameover_on_exit = args.gameover_on_exit,
             scores_file= args.scores_file
             ).start()

    except SnakeError as e:
        print(f"Error: {e}") # noqa: T201
        sys.exit(1)
