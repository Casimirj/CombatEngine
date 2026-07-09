from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

NONE = Prayer(
    name="None",
    label="None",
    aliases=["none", "no prayer"],
)
PrayerRegistry.register(NONE)
