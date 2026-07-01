from app.GameDefinitions.Prayer import Prayer
from app.Registries.PrayerRegistry import PrayerRegistry
BURST_OF_STRENGTH = Prayer(
    name="Burst of Strength", label="Burst of Strength",
    attack_multiplier=1.05, strength_multiplier=1.05,
    aliases=["burst of strength", "burst"],
)
PrayerRegistry.register(BURST_OF_STRENGTH)
