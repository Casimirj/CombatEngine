import warnings
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
class DynamicAttack:
    """Sentinel indicating this attack slot is resolved at runtime."""


@dataclass
class AttackSchedule:
    """A named sequence of Attack objects for a boss phase."""

    name: str
    rotation: List[Attack] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("AttackSchedule name cannot be empty")

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
        raise NotImplementedError

    def get_next_attack(self, idx: int, room_state) -> Attack:
        attack = self.rotation[idx]
        if isinstance(attack, DynamicAttack):
            warnings.warn(
                f"{type(self).__name__}.get_next_attack() not overridden — "
                f"DynamicAttack at idx {idx} will be returned as-is, "
                f"which will likely cause a runtime error."
            )
        return attack

    # ── Gear switching ────────────────────────────────────────────────────

    def _equip_setup(self, player, setup: Setup) -> None:
        """Clear current gear and equip a new phase setup."""
        player.clear_gear()
        gear_pieces = [GearRegistry.get(name) for name in setup.pieces]
        player.equip_gear(*gear_pieces)
        player.prayer = PrayerRegistry.get(setup.prayer)
        player.boosts = [PotionRegistry.get(b) for b in setup.boosts] if setup.boosts else []
