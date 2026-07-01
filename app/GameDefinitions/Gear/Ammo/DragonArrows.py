from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class DragonArrows(Gear):
    name = "Dragon arrows"
    slot = GearSlot.AMMO
    aliases = ["dragon arrows", "dragon arrow"]
    ammo_category = "arrows"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 60,
        }


GearRegistry.register(DragonArrows())
