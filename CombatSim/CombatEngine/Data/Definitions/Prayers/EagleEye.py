from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

EAGLE_EYE = Prayer(
    name="Eagle Eye",
    label="Eagle Eye",
    ranged_attack_multiplier=1.15,
    ranged_strength_multiplier=1.15,
    aliases=["eagle eye"],
)
PrayerRegistry.register(EAGLE_EYE)
