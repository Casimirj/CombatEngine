from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class BandosTassets(Gear):
    name = "Bandos tassets"
    slot = GearSlot.LEGS
    aliases = ["bandos tassets", "bandos legs", "tassets"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -21,
            "ranged_attack_bonus": -7,
            "melee_strength_bonus":  2,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  71,
            "slash_def":  63,
            "crush_def":  66,
            "magic_def": -4,
            "ranged_def_light":  93,
            "ranged_def_med":  93,
            "prayer_bonus": 1,
            "ranged_def_heavy":  93}


GearRegistry.register(BandosTassets())

