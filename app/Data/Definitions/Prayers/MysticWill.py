from app.Domain.Prayer import Prayer
from app.Data.Registries.PrayerRegistry import PrayerRegistry

MYSTIC_WILL = Prayer(
    name="Mystic Will",
    label="Mystic Will",
    magic_attack_multiplier=1.05,
    aliases=["mystic will"],
)
PrayerRegistry.register(MYSTIC_WILL)
