from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

IMPROVED_REFLEXES = Prayer(
    name="Improved Reflexes",
    label="Improved Reflexes",
    attack_multiplier=1.10,
    aliases=["improved reflexes"],
)
PrayerRegistry.register(IMPROVED_REFLEXES)
