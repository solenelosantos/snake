import enum

class State(enum.Enum):
    QUIT=0
    PLAY=1
    GAMEOVER=2
    SCORES=3
    INPUT_NAME=4