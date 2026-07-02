from app.Domain.Prayer import Prayer
from app.Data.Registries.PrayerRegistry import PrayerRegistry

CLARITY_OF_THOUGHT = Prayer(
    name="Clarity of Thought",
    label="Clarity of Thought",
    attack_multiplier=1.05,
    aliases=["clarity of thought", "clarity"],
)
PrayerRegistry.register(CLARITY_OF_THOUGHT)
