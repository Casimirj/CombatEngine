from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

MYSTIC_VIGOUR = Prayer(
    name="Mystic Vigour",
    label="Mystic Vigour",
    magic_attack_multiplier=1.18,
    magic_damage_bonus=0.03,
    aliases=["mystic vigour", "mystic vigor"],
)
PrayerRegistry.register(MYSTIC_VIGOUR)
