from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class DragonDarts(Gear):
    name = "Dragon darts"
    slot = GearSlot.AMMO
    aliases = ["dragon darts", "dragon dart"]
    ammo_category = "darts"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 35,
        }


GearRegistry.register(DragonDarts())
