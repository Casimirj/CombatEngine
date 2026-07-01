from app.GameDefinitions.Prayer import Prayer
from app.Registries.PrayerRegistry import PrayerRegistry
SUPERNATURAL_STRENGTH = Prayer(
    name="Superhuman Strength", label="Superhuman Strength",
    strength_multiplier=1.10,
    aliases=["superhuman strength", "superhuman", "SUPERNATURAL_STRENGTH", "supernatural strength"],
)
PrayerRegistry.register(SUPERNATURAL_STRENGTH)
