from dataclasses import dataclass, field
from typing import List, Optional, Type

from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry


@dataclass
class Setup:
    """Bundles gear pieces, prayer, and boosts for a single phase."""
    pieces: List[str]
    prayer: str
    boosts: List[str] = field(default_factory=list)


@dataclass
class Attack:
    """A single attack in a schedule.

    If ``setup`` is provided, gear/prayer/boosts are swapped before the
    attack is executed.  When ``None`` the player keeps whatever is
    currently equipped.
    """

    weapon: Type[Weapon]
    setup: Optional[Setup] = None
    use_special_attack: bool = False
    repeat: bool = False


@dataclass
class AttackSchedule:
    """A named sequence of Attack objects for a boss phase.

    Subclasses override ``update_rotation`` to rebuild the rotation when
    the boss phase or room state changes.
    """

    name: str
    rotation: List[Attack] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("AttackSchedule name cannot be empty")
        if not self.rotation:
            raise ValueError("AttackSchedule rotation cannot be empty")

    def __len__(self) -> int:
        return len(self.rotation)

    def __getitem__(self, index: int) -> Attack:
        return self.rotation[index]

    def __repr__(self) -> str:
        return f"AttackSchedule(name={self.name!r}, len={len(self.rotation)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AttackSchedule):
            return NotImplemented
        return self.name == other.name and self.rotation == other.rotation

    def update_rotation(self, room_state) -> None:
        """Rebuild the rotation for a new boss phase.

        Override in subclasses.  The *room_state* type is boss-specific;
        the sim loop passes whatever state object the boss defines.
        """
        raise NotImplementedError

    # ── Gear switching ────────────────────────────────────────────────────

    def _equip_setup(self, player, setup: Setup) -> None:
        """Clear current gear and equip a new phase setup."""
        player.clear_gear()
        gear_pieces = [GearRegistry.get(name) for name in setup.pieces]
        player.equip_gear(*gear_pieces)
        player.prayer = PrayerRegistry.get(setup.prayer)
        player.boosts = [PotionRegistry.get(b) for b in setup.boosts] if setup.boosts else []
