from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class RuneArrows(Gear):
    name = "Rune arrows"
    slot = GearSlot.AMMO
    aliases = ["rune arrows", "rune arrow"]
    ammo_category = "arrows"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 49,
        }


GearRegistry.register(RuneArrows())
