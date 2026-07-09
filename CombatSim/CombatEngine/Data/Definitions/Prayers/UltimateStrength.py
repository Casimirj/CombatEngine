from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

ULTIMATE_STRENGTH = Prayer(
    name="Ultimate Strength",
    label="Ultimate Strength",
    strength_multiplier=1.15,
    aliases=["ultimate strength"],
)
PrayerRegistry.register(ULTIMATE_STRENGTH)
