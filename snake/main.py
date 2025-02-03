import sys

# First party
from snake.lignecommande import lignecommande
from snake.exceptions import SnakeError
from snake.game import Game
from snake.score import Score
from snake.scores import Scores

def main() -> None:

    try:
        # Read command line arguments
        args = lignecommande()

        # Load scores from the YAML file
        scores = Scores.load("high_scores.yaml")

        # Start game
        game=Game(width = args.width, height = args.height,
             tile_size = args.tile_size, fps = args.fps,
             fruit_color = args.fruit_color,
             snake_head_color = args.snake_head_color,
             snake_body_color = args.snake_body_color,
             gameover_on_exit = args.gameover_on_exit,
             ).start()
        
        # After the game, handle the player's score
        #if game.is_game_over(): 
            # Ask for player's name and add score to the scores list
            #player_name = input("Enter your name: ")
            #player_score = game.get_player_score()  # Récupère le score du joueur
            #player_score_obj = Score(score=player_score, name=player_name)
            #scores.add_score(player_score_obj)

            # Save updated scores to the file
            #scores.save("high_scores.yaml")

    except SnakeError as e:
        print(f"Error: {e}") # noqa: T201
        sys.exit(1)
