from app.Domain.Enums.AmmoType import AmmoType
from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


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
