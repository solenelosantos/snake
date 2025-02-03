import abc



class Observer(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    def notify_object_eaten(self, obj: "GameObject") -> None:
        pass
# C'est le snake qui appelle cette méthode
    def notify_object_moved(self, obj: "GameObject") -> None:
        pass
# C'est le Board qui appelle le fruit et le snake.
    def notify_collision(self, obj: "GameObject") -> None:
        pass