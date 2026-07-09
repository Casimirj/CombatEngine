from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

RIGOUR = Prayer(
    name="Rigour",
    label="Rigour",
    defence_multiplier=1.25,
    ranged_attack_multiplier=1.20,
    ranged_strength_multiplier=1.23,
    aliases=["rigour"],
)
PrayerRegistry.register(RIGOUR)
