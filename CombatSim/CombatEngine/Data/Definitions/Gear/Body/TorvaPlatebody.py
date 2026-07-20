from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class TorvaPlatebody(Gear):
    name = "Torva platebody"
    slot = GearSlot.BODY
    aliases = ["torva body", "torva plate", "torva platebody"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -18,
            "ranged_attack_bonus": -14,
            "melee_strength_bonus":  6,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  117,
            "slash_def":  111,
            "crush_def":  117,
            "magic_def": -11,
            "ranged_def_light":  142,
            "ranged_def_med":  142,
            "prayer_bonus": 1,
            "ranged_def_heavy":  142}


GearRegistry.register(TorvaPlatebody())

