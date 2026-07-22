from abc import ABC, abstractmethod

from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot


class Gear(ABC):
    """Abstract base for a piece of gear.

    Subclasses define a name, a slot, optional aliases, and implement
    ``build()`` to return a stats dict. Override ``player_kwargs`` for
    extra Player constructor arguments (e.g. ``wearing_salve``).
    """

    name: str
    slot: GearSlot
    aliases: list[str] = []
    min_hit: int = 1
    player_kwargs: dict = {}

    @abstractmethod
    def build(self) -> dict:
        """Return a dict of stat key → value to merge into the Player's stats."""
        ...
