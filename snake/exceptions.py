

class SnakeException (Exception):
    def __init__(self, message :str)->None:
        super().__init__(message)

class SnakeError( SnakeException):
    def __init__(self, message :str)->None:
        super().__init__(message)

class IntRangeError(SnakeError):
    def __init__(self, name: str, value:int, Vmin: int, Vmax: int)-> None:
        super().__init__(f"Value {value} is out of allowed range [{Vmin}-{Vmax}].")

class ColorError(SnakeError):
    def __init__(self, bad_color: str, name :str):
        super().__init__(f"Wrong color {bad_color} for argument name.")

class GameOver (SnakeException):
    def __init__(self):
        super().__init__(f'Game over')
