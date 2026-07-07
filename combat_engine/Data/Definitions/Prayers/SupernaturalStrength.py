from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

SUPERNATURAL_STRENGTH = Prayer(
    name="Superhuman Strength",
    label="Superhuman Strength",
    strength_multiplier=1.10,
    aliases=["superhuman strength", "superhuman", "SUPERNATURAL_STRENGTH", "supernatural strength"],
)
PrayerRegistry.register(SUPERNATURAL_STRENGTH)
