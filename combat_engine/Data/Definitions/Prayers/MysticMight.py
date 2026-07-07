from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

MYSTIC_MIGHT = Prayer(
    name="Mystic Might",
    label="Mystic Might",
    magic_attack_multiplier=1.15,
    magic_damage_bonus=0.02,
    aliases=["mystic might"],
)
PrayerRegistry.register(MYSTIC_MIGHT)
