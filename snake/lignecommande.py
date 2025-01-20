import argparse
import re
from .exceptions import ColorError
from pathlib import Path

DEFAULT_WIDTH= 400
DEFAULT_HEIGHT= 300
DEFAULT_PIXEL= 22
SNAKE_POSITION = [10,5]
FPS_MIN=5
FPS_MAX=25
HEIGHT_MIN=200
HEIGHT_MAX=400

def lignecommande():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, help="columns number", default=DEFAULT_WIDTH)
    parser.add_argument('-H','--height', type=int, help= "ligns number", default=DEFAULT_HEIGHT)
    parser.add_argument('--tile_size', type=int, help="size of a tile", default=DEFAULT_PIXEL)
    parser.add_argument('--fps', '--framepersecond', type=int, help= "number of frames per second", default=10)
    parser.add_argument( '--fruit_color', type=str, help= "color of the fruit", default= '#ff0000' )
    parser.add_argument('--snake_head_color', type=str, help="color of the head's snake", default='#ffffff')
    parser.add_argument( '--snake_body_color', type=str, help="color of the body's snake", default='#00ff00')
    parser.add_argument('--tc', '--text_color', type=str, help='color of the text', default="#ff6eb4")
    parser.add_argument('--ms', '--max_scores', type= str, help = 'max of scores', default= 5 )
    parser.add_argument('-sf', '--scores_file', type=Path, help = 'file which saves and loads the scores', default="snake_scores.yml")
     # Game options
    parser.add_argument("--gameover_on_exit", action = "store_true",
                        help="Exiting the board ends the game.")
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