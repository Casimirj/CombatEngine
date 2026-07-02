from app.Domain.Enums.AmmoType import AmmoType
from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class DragonArrows(Gear):
    name = "Dragon arrows"
    slot = GearSlot.AMMO
    aliases = ["dragon arrows", "dragon arrow"]
    ammo_category = AmmoType.ARROWS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 60,
        }


GearRegistry.register(DragonArrows())
