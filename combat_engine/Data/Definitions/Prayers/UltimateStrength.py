from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

ULTIMATE_STRENGTH = Prayer(
    name="Ultimate Strength",
    label="Ultimate Strength",
    strength_multiplier=1.15,
    aliases=["ultimate strength"],
)
PrayerRegistry.register(ULTIMATE_STRENGTH)
