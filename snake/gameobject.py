import pygame
import abc
from .subject import Subject
from .observer import Observer
from typing import NoReturn

class GameObject(Subject, Observer): #il vaut mieux mettre Subject en premier. Subject=class, Observeur= interface
    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> NoReturn: 
        raise NotImplementedError

    @property
    def background(self):
        return False #by default, a gameobject is not a background

    def __contains__(self, obj :"GameObject")-> bool:
        if isinstance(obj, GameObject):
            return any(t in obj.tiles for t in self.tiles)
        return False