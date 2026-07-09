from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class DragonDarts(Gear):
    name = "Dragon darts"
    slot = GearSlot.AMMO
    aliases = ["dragon darts", "dragon dart"]
    ammo_category = AmmoType.DARTS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 35,
        }


GearRegistry.register(DragonDarts())
