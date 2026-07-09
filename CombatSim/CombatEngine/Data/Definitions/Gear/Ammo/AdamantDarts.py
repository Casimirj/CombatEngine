from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class AdamantDarts(Gear):
    name = "Adamant darts"
    slot = GearSlot.AMMO
    aliases = ["adamant darts", "adamant dart", "addy darts", "add darts"]
    ammo_category = AmmoType.DARTS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 17,
        }


GearRegistry.register(AdamantDarts())
