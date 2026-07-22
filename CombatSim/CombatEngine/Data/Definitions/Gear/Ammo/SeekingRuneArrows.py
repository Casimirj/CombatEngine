from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class SeekingRuneArrows(Gear):
    name = "Seeking rune arrows"
    slot = GearSlot.AMMO
    aliases = ["seeking rune arrows", "seeking rune arrow",
               "s rune", "seeking rune"]
    ammo_category = AmmoType.ARROWS
    min_hit = 3

    def build(self) -> dict:
        return {
            "ranged_attack_bonus": 20,
            "ranged_strength_bonus": 49,
        }


GearRegistry.register(SeekingRuneArrows())
