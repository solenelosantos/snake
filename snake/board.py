
import typing

from snake.subject import Subject
from snake.observer import Observer
from snake.fruit import Fruit
from snake.gameobject import GameObject



class Board (Subject, Observer) : # subject car le Board reçoit aussi des infos des objets. 
    def __init__(self, screen, tile_size, nb_rows, nb_cols) -> None:
        super().__init__()
        self._screen= screen
        self._tile_size= tile_size
        self._objects : list[GameObject]=[]
        self._nb_rows= nb_rows
        self._nb_cols= nb_cols

    def add_object(self,gameobject: GameObject):
        if gameobject not in self._objects:
            self._objects.append(gameobject)
            gameobject.attach_obs(self) #permet au board de devenir l'observeur des objects ajoutés.

    def remove_object(self, gameobject: GameObject):
        if gameobject in self._objects:
            gameobject.detach_obs(self) # le board n'est plus l'observateur de l'object.
            self._object.remove(gameobject)

    def create_fruit(self)-> "Fruit":
        fruit = None
        while fruit is None or list(self.detect_collision(fruit)):
            fruit= Fruit.create_random(self._nb_rows, self._nb_cols)
        self.add_object(fruit)

    def draw(self) -> None:
        """Draw all objects on screen."""
        # Loop on all objects
        for obj in self._objects:
            # Loop on all object's tiles
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def detect_collision(self, obj: "GameObject")-> typing.Iterator[GameObject]:
        # Loop on all known objects
        for o in self._objects:

            # Detect a collision
            if obj != o and not o.background and obj in o:
                yield o

    def notify_object_moved(self, obj: "GameObject")-> None:
        o=self.detect_collision(obj)
        if not o is None:
                obj.notify_collision(o)

    def notify_object_eaten(self, obj: "GameObject")-> None:
        self.remove_object(obj) # Remove the fruit eaten
        self.create_fruit()