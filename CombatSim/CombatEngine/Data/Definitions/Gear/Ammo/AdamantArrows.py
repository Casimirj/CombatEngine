from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


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
