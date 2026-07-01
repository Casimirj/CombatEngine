from app.GameDefinitions.Prayer import Prayer
from app.Registries.PrayerRegistry import PrayerRegistry
MYSTIC_LORE = Prayer(
    name="Mystic Lore", label="Mystic Lore",
    magic_attack_multiplier=1.10, magic_damage_bonus=0.01,
    aliases=["mystic lore"],
)
PrayerRegistry.register(MYSTIC_LORE)
