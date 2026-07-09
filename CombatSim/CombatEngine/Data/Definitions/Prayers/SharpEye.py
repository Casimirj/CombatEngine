from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

SHARP_EYE = Prayer(
    name="Sharp Eye",
    label="Sharp Eye",
    ranged_attack_multiplier=1.05,
    ranged_strength_multiplier=1.05,
    aliases=["sharp eye"],
)
PrayerRegistry.register(SHARP_EYE)
