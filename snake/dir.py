import enum

class Dir(enum.Enum):
    UP=(0,-1)
    DOWN=(0,1)
    RIGHT=(1,0)
    LEFT=(-1,0)

    @property
    def x(self) -> int:
        """Column index (starts at 0)."""
        return self.value[0]

    @property
    def y(self) -> int:
        """Line index (starts at 0)."""
        return self.value[1]
