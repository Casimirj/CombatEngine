from app.Domain.Enums.AmmoType import AmmoType
from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class RuneArrows(Gear):
    name = "Rune arrows"
    slot = GearSlot.AMMO
    aliases = ["rune arrows", "rune arrow"]
    ammo_category = AmmoType.ARROWS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 49,
        }


GearRegistry.register(RuneArrows())
