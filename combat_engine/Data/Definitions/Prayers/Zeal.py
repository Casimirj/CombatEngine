from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

ZEAL = Prayer(
    name="Zeal",
    label="Zeal",
    attack_multiplier=1.25,
    strength_multiplier=1.28,
    defence_multiplier=1.25,
    aliases=["zeal"],
)
PrayerRegistry.register(ZEAL)
