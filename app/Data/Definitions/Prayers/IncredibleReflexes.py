from app.Domain.Prayer import Prayer
from app.Data.Registries.PrayerRegistry import PrayerRegistry

INCREDIBLE_REFLEXES = Prayer(
    name="Incredible Reflexes",
    label="Incredible Reflexes",
    attack_multiplier=1.15,
    aliases=["incredible reflexes"],
)
PrayerRegistry.register(INCREDIBLE_REFLEXES)
