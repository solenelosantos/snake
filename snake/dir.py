import enum

class Dir(enum.Enum):
    UP=(0,-1)
    DOWN=(0,1)
    RIGHT=(1,0)
    LEFT=(-1,0)