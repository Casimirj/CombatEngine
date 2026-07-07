from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

MYSTIC_LORE = Prayer(
    name="Mystic Lore",
    label="Mystic Lore",
    magic_attack_multiplier=1.10,
    magic_damage_bonus=0.01,
    aliases=["mystic lore"],
)
PrayerRegistry.register(MYSTIC_LORE)
