from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class RuneDarts(Gear):
    name = "Rune darts"
    slot = GearSlot.AMMO
    aliases = ["rune darts", "rune dart"]
    ammo_category = "darts"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 26,
        }


GearRegistry.register(RuneDarts())
