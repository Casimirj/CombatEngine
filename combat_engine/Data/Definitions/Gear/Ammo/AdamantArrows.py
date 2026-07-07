from combat_engine.Domain.Enums.AmmoType import AmmoType
from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class AdamantArrows(Gear):
    name = "Adamant arrows"
    slot = GearSlot.AMMO
    aliases = ["adamant arrows", "adamant arrow", "addy arrows", "add arrows"]
    ammo_category = AmmoType.ARROWS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 31,
        }


GearRegistry.register(AdamantArrows())
