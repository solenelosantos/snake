

class Observer():
    """Interface representing an observer for the Observer pattern."""

    def __init__(self) -> None:
        """Object initialization."""
        super().__init__()

    def notify_object_moved(self, obj: "GameObject") -> None:
        """Notify that an object has moved."""

    def notify_collision(self, obj: "GameObject") -> None:
        """Notify that an object collides with another."""

    def notify_object_eaten(self, obj: "GameObject") -> None:
        """Notify that an object is eaten."""