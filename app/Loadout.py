from abc import ABC, abstractmethod

from app.Player import Player


class Loadout(ABC):
    """Abstract base for a gear loadout.

    Subclasses define a name, optional aliases, and implement ``build()``
    to return a fully equipped ``Player``.
    """

    name: str
    aliases: list[str] = []

    @abstractmethod
    def build(self) -> Player: ...
