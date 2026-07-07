from combat_engine.Domain.Enums.AmmoType import AmmoType
from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class AmethystArrows(Gear):
    name = "Amethyst arrows"
    slot = GearSlot.AMMO
    aliases = ["amethyst arrows", "amethyst arrow", "ame arrows"]
    ammo_category = AmmoType.ARROWS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 55,
        }


GearRegistry.register(AmethystArrows())
